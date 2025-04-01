import uuid


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """
    PDFバイナリをMarkdownテキストに変換する。

    Args:
        pdf_bytes (bytes): アップロードされたPDFファイルの中身

    Returns:
        str: Markdown形式の全文
    """
    # TODO: 実装例（pymupdf4llmなどのライブラリを使用）
    return "# Sample Markdown\n本文の例です。"


def chunk_markdown(markdown: str) -> list[dict]:
    """
    Markdownテキストを再帰的にチャンク化し、chunk_id付きリストで返す。

    Args:
        markdown (str): Markdownテキスト

    Returns:
        list[dict]: チャンク化されたテキストとメタ情報のリスト
    """
    # 簡易分割（TODO: 再帰的分割に置き換え）
    lines = markdown.splitlines()
    chunks = []
    chunk = ""
    for line in lines:
        if line.startswith("#"):
            if chunk:
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk.strip(),
                    "chapter": "不明",
                    "position": len(chunks) + 1
                })
                chunk = ""
        chunk += line + "\n"
    if chunk:
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": chunk.strip(),
            "chapter": "最終",
            "position": len(chunks) + 1
        })
    return chunks
