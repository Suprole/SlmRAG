from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services import retriever, generator, models
import json

router = APIRouter()


class ChatQuery(BaseModel):
    document_id: str
    query: str


@router.post("/chat")
def chat(query: ChatQuery):
    if not models.document_exists(query.document_id):
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = retriever.retrieve_top_chunks(query.document_id, query.query)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant chunks found")

    async def generate():
        answer, citations = generator.generate_answer(query.query, chunks)
        yield json.dumps({"answer": answer, "citations": citations}) + "\n"

    return StreamingResponse(generate(), media_type="application/json")
