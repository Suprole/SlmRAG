"""
In-memory storage service for Hugging Face deployment

This module provides in-memory alternatives to the file-based storage
methods used in the standard version of the application.
"""
import os
from typing import Dict, List, Any, Optional
import faiss
import numpy as np
from .logger import Logger

# Initialize logger
logger = Logger(name="memory_store")

# In-memory storage
markdown_store: Dict[str, str] = {}
faiss_index_store: Dict[str, faiss.Index] = {}
chunk_id_store: Dict[str, List[str]] = {}

def is_huggingface_space() -> bool:
    """Check if running on HF Spaces"""
    return os.environ.get("SPACE_ID") is not None

def store_markdown(document_id: str, markdown: str) -> None:
    """Store markdown in memory"""
    if is_huggingface_space():
        logger.info(f"Storing markdown for document {document_id} in memory")
        markdown_store[document_id] = markdown
    else:
        # Fall back to file storage for local development
        os.makedirs("data/markdown", exist_ok=True)
        md_path = f"data/markdown/{document_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

def get_markdown(document_id: str) -> Optional[str]:
    """Get markdown from memory or file"""
    if is_huggingface_space():
        return markdown_store.get(document_id)
    else:
        md_path = f"data/markdown/{document_id}.md"
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

def store_faiss_index(document_id: str, index: faiss.Index, chunk_ids: List[str]) -> None:
    """Store FAISS index in memory"""
    if is_huggingface_space():
        logger.info(f"Storing FAISS index for document {document_id} in memory")
        faiss_index_store[document_id] = index
        chunk_id_store[document_id] = chunk_ids
    else:
        # Fall back to file storage for local development
        os.makedirs("data/faiss", exist_ok=True)
        index_path = f"data/faiss/{document_id}.index"
        meta_path = f"data/faiss/{document_id}.index.meta"
        
        import json
        faiss.write_index(index, index_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(chunk_ids, f)

def get_faiss_index(document_id: str) -> Optional[tuple[faiss.Index, List[str]]]:
    """Get FAISS index from memory or file"""
    if is_huggingface_space():
        if document_id in faiss_index_store and document_id in chunk_id_store:
            return faiss_index_store[document_id], chunk_id_store[document_id]
        return None
    else:
        import json
        index_path = f"data/faiss/{document_id}.index"
        meta_path = f"data/faiss/{document_id}.index.meta"
        
        if os.path.exists(index_path) and os.path.exists(meta_path):
            index = faiss.read_index(index_path)
            with open(meta_path, "r", encoding="utf-8") as f:
                chunk_ids = json.load(f)
            return index, chunk_ids
        return None

def delete_document_data(document_id: str) -> None:
    """Delete document data from memory"""
    if is_huggingface_space():
        logger.info(f"Removing document {document_id} from memory")
        if document_id in markdown_store:
            del markdown_store[document_id]
        if document_id in faiss_index_store:
            del faiss_index_store[document_id]
        if document_id in chunk_id_store:
            del chunk_id_store[document_id]
    else:
        # Delete from file system
        md_path = f"data/markdown/{document_id}.md"
        index_path = f"data/faiss/{document_id}.index"
        meta_path = f"data/faiss/{document_id}.index.meta"
        
        for path in [md_path, index_path, meta_path]:
            if os.path.exists(path):
                os.remove(path)