from pathlib import Path
from typing import List
from haystack.components.converters import TextFileToDocument, PyPDFToDocument
from haystack.dataclasses import Document


def load_txt(file_path: str) -> List[Document]:
    converter = TextFileToDocument()
    result = converter.run(sources=[file_path])
    return result["documents"]


def load_pdf(file_path: str) -> List[Document]:
    converter = PyPDFToDocument()
    result = converter.run(sources=[file_path])
    return result["documents"]


def load_document(file_path: str) -> List[Document]:
    ext = Path(file_path).suffix.lower()
    print("        =       " + ext  + "        =   ")
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"Formato não suportado: {ext}")
