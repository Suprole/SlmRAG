import uuid
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pymupdf4llm
import tempfile
import os
from .logger import Logger

# ロガーの初期化
logger = Logger(name="pdf_processor")


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """
    PDFバイナリを一時ファイルとして保存し、pymupdf4llmでMarkdownに変換。

    Args:
        pdf_bytes (bytes): PDFファイルのバイナリ

    Returns:
        str: Markdown形式の全文
    """
    logger.info(f"PDFからMarkdownへの変換開始: サイズ {len(pdf_bytes)} bytes")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        temp_path = tmp.name
        logger.debug(f"一時ファイルに保存: {temp_path}")
        
        try:
            md = pymupdf4llm.to_markdown(temp_path)
            logger.debug(f"Markdown変換完了: 文字数 {len(md)}")
            return md
        finally:
            # 一時ファイルの削除
            try:
                os.unlink(temp_path)
                logger.debug(f"一時ファイルを削除: {temp_path}")
            except Exception as e:
                logger.warning(f"一時ファイルの削除に失敗: {e}")



def chunk_markdown(markdown: str) -> List[Dict]:
    """
    Markdownを再帰的にチャンク化してchunk_id付きで返す。

    Args:
        markdown (str): Markdownテキスト

    Returns:
        list[dict]: チャンク情報のリスト
    """
    logger.info(f"Markdownのチャンク化開始: 文字数 {len(markdown)}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "、", " ", ""]
    )
    logger.debug("テキストスプリッターを初期化: チャンクサイズ=100, オーバーラップ=20")
    
    docs = splitter.create_documents([markdown])
    logger.debug(f"ドキュメント分割完了: {len(docs)}個のチャンクを生成")

    chunks = []
    for i, doc in enumerate(docs):
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": doc.page_content.strip(),
            "chapter": "N/A",  # 後で章解析ロジックがあれば付与
            "position": i + 1
        })
    
    logger.info(f"Markdownのチャンク化完了: {len(chunks)}個のチャンクを生成")
    return chunks

if __name__ == "__main__":
    logger.debug("pdf_processor直接実行")
    pass