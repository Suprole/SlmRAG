import uuid
from typing import List, Dict
import tempfile
import os
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from .logger import Logger
import sys
import json
import re
from abc import ABC, abstractmethod
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core import Document
from llama_index.core.schema import TextNode

class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        pass

class MarkdownHeaderChunker(Chunker):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.sub_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "、", " "]
        )
        self.header_pattern = re.compile(r"^#{1,6} .*", re.MULTILINE)

    def chunk(self, text: str) -> List[str]:
        headers = list(self.header_pattern.finditer(text))
        if not headers:
            return self.sub_splitter.split_text(text)

        sections = []
        for i, match in enumerate(headers):
            start = match.start()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            sections.append(text[start:end])

        chunks = []
        for section in sections:
            chunks.extend(self.sub_splitter.split_text(section))
        return chunks

# ロガーの初期化
logger = Logger(name="pdf_processor")


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """
    PDFバイナリを一時ファイルとして保存し、markerでMarkdownに変換。

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
            converter = PdfConverter(
                artifact_dict=create_model_dict(),
            )
            rendered = converter(temp_path)
            markdown, _, _ = text_from_rendered(rendered)
            logger.debug(f"Markdown変換完了: 文字数 {len(markdown)}")
            return markdown
        finally:
            # 一時ファイルの削除
            try:
                os.unlink(temp_path)
                logger.debug(f"一時ファイルを削除: {temp_path}")
            except Exception as e:
                logger.warning(f"一時ファイルの削除に失敗: {e}")



def chunk_markdown(markdown: str) -> List[Dict]:
    """
    Markdownをヘッダーベースでチャンク化してchunk_id付きで返す。

    Args:
        markdown (str): Markdownテキスト

    Returns:
        list[dict]: チャンク情報のリスト
    """
    logger.info(f"Markdownのチャンク化開始: 文字数 {len(markdown)}")
    
    # MarkdownHeaderChunkerの初期化（最適なチャンクサイズとオーバーラップを設定）
    chunker = MarkdownHeaderChunker(chunk_size=800, chunk_overlap=150)
    logger.debug("MarkdownHeaderChunker初期化: チャンクサイズ=800, オーバーラップ=150")
    
    # チャンク化実行
    text_chunks = chunker.chunk(markdown)
    logger.debug(f"ドキュメント分割完了: {len(text_chunks)}個のチャンクを生成")

    chunks = []
    for i, text in enumerate(text_chunks):
        # ヘッダー情報を抽出する試み
        chapter = "N/A"
        # 最初の行がヘッダーかどうかをチェック
        header_lines = [line for line in text.split('\n') if line.strip().startswith('#')]
        if header_lines:
            chapter = header_lines[0].strip('# ')
        
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": text.strip(),
            "chapter": chapter,
            "position": i + 1
        })
    
    logger.info(f"Markdownのチャンク化完了: {len(chunks)}個のチャンクを生成")
    return chunks

if __name__ == "__main__":
    logger.debug("pdf_processor直接実行")
    pass