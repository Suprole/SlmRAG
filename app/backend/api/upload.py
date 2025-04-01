from fastapi import APIRouter, UploadFile, File, HTTPException
from services import pdf_processor, embedder, faiss_manager, models
import uuid
import os
from datetime import datetime

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # 1. 読み込み
        content = await file.read()
        document_id = str(uuid.uuid4())
        title = file.filename

        # 2. Markdown変換
        markdown = pdf_processor.convert_pdf_to_markdown(content)
        os.makedirs("data/markdown", exist_ok=True)
        md_path = f"data/markdown/{document_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        # 3. チャンク化
        chunks = pdf_processor.chunk_markdown(markdown)

        # 4. ベクトル化
        embeddings = []
        for chunk in chunks:
            vector = embedder.vectorize_text(chunk["text"])
            embeddings.append({**chunk, "vector": vector})

        # 5. FAISSインデックス作成
        faiss_manager.create_index(document_id, embeddings)

        # 6. DB登録
        models.insert_document(document_id, title, created_at=datetime.utcnow())
        for chunk in chunks:
            models.insert_chunk(
                chunk_id=chunk["chunk_id"],
                document_id=document_id,
                chapter=chunk["chapter"],
                position=chunk["position"],
                text=chunk["text"]
            )

        return {"document_id": document_id, "title": title, "chunks": len(chunks)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
