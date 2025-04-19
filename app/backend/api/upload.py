from fastapi import APIRouter, UploadFile, File, HTTPException
from services import pdf_processor, embedder, faiss_manager, models, memory_store
import uuid
import os
from datetime import datetime

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDFファイルのみアップロード可能です。")

    try:
        # 1. PDFファイルの読み込み
        content = await file.read()
        document_id = str(uuid.uuid4())
        title = file.filename

        # 2. PDFをMarkdownに変換（marker-pdfを使用）
        markdown = pdf_processor.convert_pdf_to_markdown(content)
        
        # Store markdown in memory or file system based on environment
        memory_store.store_markdown(document_id, markdown)

        # 3. MarkdownをMarkdownHeaderChunkerを使用してチャンク化
        chunks = pdf_processor.chunk_markdown(markdown)

        # 4. 各チャンクをベクトル化
        embeddings = []
        for chunk in chunks:
            vector = embedder.vectorize_text(chunk["text"])
            embeddings.append({**chunk, "vector": vector})

        # 5. FAISSインデックスを作成して保存
        faiss_manager.create_index(document_id, embeddings)

        # 6. ドキュメント情報とチャンクをDBに登録
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
        raise HTTPException(status_code=500, detail=f"アップロード処理中にエラーが発生しました: {str(e)}")
