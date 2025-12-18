from elasticsearch import Elasticsearch, exceptions
import os
import time

INDEX_NAME = "rag_chunks"

class ElasticRepository:
    def __init__(self):
        elastic_url = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
        self.client = Elasticsearch(elastic_url)

 
        self._wait_for_elasticsearch()

    def _wait_for_elasticsearch(self, retries=10, delay=3):
        for i in range(retries):
            try:
                if self.client.ping():
                    print(" Elasticsearch está pronto!")
                    return
            except exceptions.ConnectionError:
                pass
            print(f" Esperando Elasticsearch... ({i+1}/{retries})")
            time.sleep(delay)
        raise RuntimeError(" Elasticsearch não está acessível após várias tentativas!")

    def create_index_if_not_exists(self):
        if not self.client.indices.exists(index=INDEX_NAME):
            self.client.indices.create(
                index=INDEX_NAME,
                body={
                    "mappings": {
                        "properties": {
                            "text": {"type": "text"},
                            "source": {"type": "keyword"},
                            "chunk_id": {"type": "integer"}
                        }
                    }
                }
            )
            print(f" Índice '{INDEX_NAME}' criado.")
        else:
            print(f"ℹ Índice '{INDEX_NAME}' já existe.")

    def index_chunk(self, chunk):
        self.client.index(
            index=INDEX_NAME,
            id=chunk.meta["chunk_uuid"],
            document={
                "text": chunk.content,
                "source": chunk.meta.get("source"),
                "chunk_id": chunk.meta.get("chunk_id")
            }
        )

    def search(self, query: str, size: int = 10):
        response = self.client.search(
            index=INDEX_NAME,
            query={"match": {"text": query}},
            size=size
        )
        return [
            {
                "text": hit["_source"]["text"],
                "score": hit["_score"]
            }
            for hit in response["hits"]["hits"]
        ]
