import sqlite3
from typing import Optional, Dict

DB_PATH = "data/db/documents.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_chunk_by_id(chunk_id: str) -> Optional[Dict]:
    """
    chunk_id に対応するチャンク情報を取得する。

    Args:
        chunk_id (str): 検索対象のチャンクID

    Returns:
        dict or None: チャンクの内容（text, chapter, position など）
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM chunks WHERE chunk_id = ?",
        (chunk_id,)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None
