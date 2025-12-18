from fastapi import FastAPI, UploadFile, File, Body, Query, HTTPException
from app.ingestion.pipeline import ingest_document
from app.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider
from app.vectorstore.qdrant_client import get_qdrant_client
from app.vectorstore.qdrant_repository import QdrantRepository
from app.search.elastic_repository import ElasticRepository
from app.search.hybrid_search import hybrid_search
from app.llm.answer_pipeline import answer_question
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import tempfile
import shutil
import os

app = FastAPI(
    title="Enterprise RAG API",
    description="API genérica de RAG para integração com sistemas corporativos",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str
    tenant: Optional[str] = "default"
    min_score: Optional[float] = 0.7
    max_chunks: Optional[int] = 5

class AnswerResponse(BaseModel):
    answer: str
    confidence: Optional[float] = None
    sources: Optional[list] = []


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }

@app.get("/info")
def service_info():
    return {
        "retrieval": "hybrid (dense + sparse)",
        "reranking": "cross-encoder",
        "llm": "groq / llama",
        "vector_db": "qdrant",
        "search": "elasticsearch"
    }

@app.post("/documents/ingest")
async def ingest_and_index(file: UploadFile = File(...)):
    tmp_path = f"/tmp/{file.filename}"

    with open(tmp_path, "wb") as tmp:
        tmp.write(await file.read())

    chunks = ingest_document(tmp_path, "upload")


    for idx, chunk in enumerate(chunks):
        chunk.meta["chunk_id"] = idx
        chunk.meta["uuid"] = str(uuid4())

    embedder = SentenceTransformerEmbeddingProvider()
    texts = [c.content for c in chunks]
    embeddings = embedder.embed(texts)

    qdrant_client = get_qdrant_client()
    qdrant_repo = QdrantRepository(qdrant_client)
    qdrant_repo.create_collection_if_not_exists(len(embeddings[0]))
    qdrant_repo.upsert_chunks(embeddings, chunks)

    elastic_repo = ElasticRepository()
    elastic_repo.create_index_if_not_exists()

    for chunk in chunks:
        elastic_repo.index_chunk(chunk)

    os.remove(tmp_path)

    return {
        "status": "indexed_hybrid",
        "chunks_indexed": len(chunks),
        "vector_dimension": len(embeddings[0]),
        "indexes": ["qdrant", "elasticsearch"]
    }


@app.get("/search")
def search(query: str):
    results = hybrid_search(query)

    return {
        "query": query,
        "results": results
    }

@app.post("/ask")
def ask_question(payload: QuestionRequest):
    if not payload.question.strip():
        raise HTTPException(
            status_code=400,
            detail="A pergunta não pode ser vazia."
        )

    result = answer_question(payload.question)

    return {
        "question": payload.question,
        "answer": result["answer"],
        "confidence": result.get("confidence", 0.0),
        "sources": result.get("sources", [])
    }
