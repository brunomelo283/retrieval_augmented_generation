from app.vectorstore.qdrant_client import get_qdrant_client
from app.search.elastic_repository import ElasticRepository
from app.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider

VECTOR_WEIGHT = 0.6
BM25_WEIGHT = 0.4
CONFIDENCE_THRESHOLD = 0.65


def hybrid_search(query: str, top_k: int = 5):
    embedder = SentenceTransformerEmbeddingProvider()
    query_vector = embedder.embed([query])[0]

    qdrant = get_qdrant_client()
    vector_results = qdrant.search(
        collection_name="rag_chunks",
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )

    elastic = ElasticRepository()
    bm25_results = elastic.search(query, size=top_k)

    max_vector = max([r.score for r in vector_results], default=1)
    max_bm25 = max([r["score"] for r in bm25_results], default=1)

    merged = {}

    for r in vector_results:
        text = r.payload["text"]
        merged[text] = (VECTOR_WEIGHT * (r.score / max_vector))

 
    for r in bm25_results:
        text = r["text"]
        merged[text] = merged.get(text, 0) + (BM25_WEIGHT * (r["score"] / max_bm25))

 
    final_results = [
        {"text": text, "score": score}
        for text, score in merged.items()
        if score >= CONFIDENCE_THRESHOLD
    ]

    
    final_results.sort(key=lambda x: x["score"], reverse=True)

    return final_results[:top_k]
