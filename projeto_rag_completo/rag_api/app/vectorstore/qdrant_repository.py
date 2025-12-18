from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List
from uuid import uuid4

COLLECTION_NAME = "rag_chunks"

class QdrantRepository:

    def __init__(self, client):
        self.client = client

    def create_collection_if_not_exists(self, vector_size: int):
        collections = self.client.get_collections().collections
        names = [c.name for c in collections]

        if COLLECTION_NAME not in names:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def upsert_chunks(self, embeddings: List[List[float]], chunks: list):
        points = []

        for embedding, chunk in zip(embeddings, chunks):
            points.append(
                PointStruct(
                    id=chunk.meta["chunk_uuid"],
                    vector=embedding,
                    payload={
                        "text": chunk.content,
                        "source": chunk.meta.get("source"),
                        "chunk_id": chunk.meta.get("chunk_id")
                    }
                )
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
