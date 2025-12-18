from typing import List
from haystack.components.preprocessors import DocumentSplitter
from haystack.dataclasses import Document


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 600,
    overlap: int = 100
) -> List[Document]:
    splitter = DocumentSplitter(
        split_by="word",
        split_length=chunk_size,
        split_overlap=overlap
    )

    result = splitter.run(documents=documents)
    return result["documents"]
