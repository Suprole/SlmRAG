from fastapi import APIRouter, HTTPException
from services import models, faiss_manager, memory_store
import os

router = APIRouter()


@router.get("/docs")
def list_documents():
    return models.get_document_list()


@router.get("/docs/{document_id}/chunks")
def get_chunks(document_id: str):
    if not models.document_exists(document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return models.get_chunks_by_document_id(document_id)


@router.delete("/docs/{document_id}")
def delete_document(document_id: str):
    if not models.document_exists(document_id):
        raise HTTPException(status_code=404, detail="Document not found")

    # DB削除
    models.delete_document(document_id)

    # FAISSインデックス削除
    try:
        faiss_manager.delete_index(document_id)
    except FileNotFoundError:
        pass

    # Markdownをメモリまたはファイルシステムから削除
    memory_store.delete_document_data(document_id)

    return {"message": f"Document {document_id} deleted."}


@router.get("/docs/{document_id}/markdown")
def get_markdown(document_id: str):
    # Try to get markdown from memory store first
    content = memory_store.get_markdown(document_id)
    
    if content is None:
        raise HTTPException(status_code=404, detail="Markdown not found")

    return {"document_id": document_id, "markdown": content}
