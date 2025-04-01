import uuid
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pymupdf4llm
import tempfile


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """
    PDFバイナリを一時ファイルとして保存し、pymupdf4llmでMarkdownに変換。

    Args:
        pdf_bytes (bytes): PDFファイルのバイナリ

    Returns:
        str: Markdown形式の全文
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        md = pymupdf4llm.to_markdown(tmp.name)
        return md



def chunk_markdown(markdown: str) -> List[Dict]:
    """
    Markdownを再帰的にチャンク化してchunk_id付きで返す。

    Args:
        markdown (str): Markdownテキスト

    Returns:
        list[dict]: チャンク情報のリスト
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "、", " ", ""]
    )
    docs = splitter.create_documents([markdown])

    chunks = []
    for i, doc in enumerate(docs):
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": doc.page_content.strip(),
            "chapter": "N/A",  # 後で章解析ロジックがあれば付与
            "position": i + 1
        })
    return chunks
