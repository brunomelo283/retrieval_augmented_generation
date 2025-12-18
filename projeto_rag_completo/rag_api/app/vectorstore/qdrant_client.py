# Exemplo do que deveria existir
from qdrant_client import QdrantClient
import os

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL", "http://qdrant:6333")        
    )
