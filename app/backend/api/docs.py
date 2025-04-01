from fastapi import APIRouter, HTTPException
from services import models, faiss_manager
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

    # Markdown削除
    md_path = f"data/markdown/{document_id}.md"
    if os.path.exists(md_path):
        os.remove(md_path)

    return {"message": f"Document {document_id} deleted."}


@router.get("/docs/{document_id}/markdown")
def get_markdown(document_id: str):
    md_path = f"data/markdown/{document_id}.md"
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Markdown not found")

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {"document_id": document_id, "markdown": content}
