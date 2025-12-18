from datetime import datetime
from uuid import uuid4
from typing import List
from haystack.dataclasses import Document

from .loaders import load_document
from .chunking import chunk_documents


def ingest_document(file_path: str, document_type: str) -> List[Document]:
    raw_docs = load_document(file_path)

    document_id = str(uuid4())
    ingested_at = datetime.utcnow().isoformat()

    for doc in raw_docs:
        doc.meta.update({
            "document_id": document_id,
            "document_type": document_type,
            "source": file_path,
            "version": 1,
            "ingested_at": ingested_at
        })

    chunks = chunk_documents(raw_docs)

    for idx, chunk in enumerate(chunks):
        chunk.meta.update({
            "chunk_id": idx,
            "chunk_uuid": str(uuid4())
        })

    return chunks
