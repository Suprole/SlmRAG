"""
チャットAPI

このモジュールは、チャットセッションの管理と
ドキュメントベースの質問応答機能を提供します。
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from services.retriever import Retriever
from services.generator import Generator

router = APIRouter(tags=["チャット"])

class ChatRequest(BaseModel):
    """チャットリクエストモデル"""
    document_id: str
    query: str
    context_size: Optional[int] = 3

class ChatResponse(BaseModel):
    """チャットレスポンスモデル"""
    answer: str
    sources: List[str]
    confidence: float

class SearchResult(BaseModel):
    """検索結果モデル"""
    text: str
    relevance: float
    page: int

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    ユーザーの質問に対して、関連ドキュメントを参照して回答を生成します。

    Args:
        request: チャットリクエスト（ドキュメントID、質問文、コンテキストサイズ）

    Returns:
        ChatResponse: 生成された回答、参照ソース、信頼度

    Raises:
        HTTPException: ドキュメントが見つからない、または処理中にエラーが発生した場合
    """
    try:
        # 関連コンテキストの取得
        retriever = Retriever()
        contexts = await retriever.retrieve(
            document_id=request.document_id,
            query=request.query,
            top_k=request.context_size
        )

        # 回答の生成
        generator = Generator()
        answer, confidence = await generator.generate_answer(
            query=request.query,
            contexts=contexts
        )

        # ソース情報の抽出
        sources = [f"ページ {ctx.page}" for ctx in contexts]

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回答生成中にエラーが発生しました: {str(e)}")

@router.post("/search", response_model=List[SearchResult])
async def search_document(request: ChatRequest):
    """
    ドキュメント内の関連部分を検索します。

    Args:
        request: 検索リクエスト（ドキュメントID、検索クエリ、結果数）

    Returns:
        List[SearchResult]: 関連テキスト、関連度スコア、ページ番号のリスト

    Raises:
        HTTPException: ドキュメントが見つからない、または検索中にエラーが発生した場合
    """
    try:
        retriever = Retriever()
        results = await retriever.retrieve(
            document_id=request.document_id,
            query=request.query,
            top_k=request.context_size
        )

        return [
            SearchResult(
                text=result.text,
                relevance=result.score,
                page=result.page
            )
            for result in results
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"検索中にエラーが発生しました: {str(e)}")
