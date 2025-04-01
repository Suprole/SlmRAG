"""
ドキュメントアップロードAPI

このモジュールは、PDFファイルのアップロード、処理、
およびベクトルデータベースへの保存を担当します。
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from services.pdf_processor import PDFProcessor
from services.embedder import Embedder
from services.faiss_manager import FAISSManager

router = APIRouter(tags=["ドキュメント管理"])

class UploadResponse(BaseModel):
    """アップロードレスポンスモデル"""
    document_id: str
    filename: str
    page_count: int
    status: str

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    PDFファイルをアップロードし、処理を行います。

    Args:
        file: アップロードされたPDFファイル

    Returns:
        UploadResponse: 処理結果と生成されたドキュメントID

    Raises:
        HTTPException: ファイル形式が不正、または処理中にエラーが発生した場合
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDFファイルのみ対応しています")

    try:
        # PDFの処理
        processor = PDFProcessor()
        document_id, page_count = await processor.process(file)

        # ベクトル埋め込みの生成と保存
        embedder = Embedder()
        vectors = await embedder.create_embeddings(document_id)

        # FAISSインデックスの更新
        faiss_manager = FAISSManager()
        await faiss_manager.add_vectors(document_id, vectors)

        return UploadResponse(
            document_id=document_id,
            filename=file.filename,
            page_count=page_count,
            status="処理完了"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ドキュメント処理中にエラーが発生しました: {str(e)}")

@router.get("/documents", response_model=List[str])
async def list_documents():
    """
    アップロードされたドキュメントの一覧を取得します。

    Returns:
        List[str]: ドキュメントIDのリスト
    """
    try:
        faiss_manager = FAISSManager()
        return await faiss_manager.list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ドキュメント一覧の取得に失敗しました: {str(e)}")
