import sqlite3
import os
from typing import Optional, Dict, List
from datetime import datetime
from .logger import Logger

# ロガーの初期化
logger = Logger(name="models")

DB_PATH = "data/db/documents.db"


def init_db():
    """
    Initialize the SQLite database with necessary tables.
    
    Creates two tables:
    - documents: Stores document metadata
    - chunks: Stores document content chunks for retrieval
    
    If the database file does not exist, it will be created.
    If the tables already exist, this function has no effect.
    """
    logger.info("データベースの初期化を開始")
    
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        logger.debug(f"データベースディレクトリを作成: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    logger.debug("documentsテーブルの作成")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        );
    """)
    
    logger.debug("chunksテーブルの作成")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            document_id TEXT,
            chapter TEXT,
            position INTEGER,
            text TEXT
        );
    """)
    
    conn.commit()
    conn.close()
    logger.info("データベースの初期化が完了しました")


def insert_document(document_id: str, title: str, created_at: datetime) -> None:
    """
    Insert a new document into the documents table.
    
    Args:
        document_id (str): Unique identifier for the document
        title (str): Title of the document
        created_at (datetime): Creation timestamp of the document
        
    Returns:
        None
    """
    logger.info(f"新規ドキュメント追加: ID「{document_id}」、タイトル「{title}」")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO documents (document_id, title, created_at) VALUES (?, ?, ?)",
            (document_id, title, created_at.isoformat())
        )
        conn.commit()
        logger.debug(f"ドキュメント追加成功: ID「{document_id}」")
    except sqlite3.Error as e:
        logger.error(f"ドキュメント追加エラー: {e}")
        raise
    finally:
        conn.close()


def insert_chunk(chunk_id: str, document_id: str, chapter: str, position: int, text: str) -> None:
    """
    Insert a document chunk into the chunks table.
    
    Args:
        chunk_id (str): Unique identifier for the chunk
        document_id (str): ID of the parent document
        chapter (str): Chapter or section name
        position (int): Numeric position in the document sequence
        text (str): Text content of the chunk
        
    Returns:
        None
    """
    logger.debug(f"チャンク追加: ID「{chunk_id}」、ドキュメントID「{document_id}」、位置: {position}")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO chunks (chunk_id, document_id, chapter, position, text) VALUES (?, ?, ?, ?, ?)",
            (chunk_id, document_id, chapter, position, text)
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"チャンク追加エラー: {e}")
        raise
    finally:
        conn.close()


def get_chunk_by_id(chunk_id: str) -> Optional[Dict]:
    """
    Retrieve a specific chunk by its ID.
    
    Args:
        chunk_id (str): ID of the chunk to retrieve
        
    Returns:
        Optional[Dict]: Dictionary containing chunk data if found, None otherwise
    """
    logger.debug(f"チャンク取得: ID「{chunk_id}」")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM chunks WHERE chunk_id = ?", (chunk_id,))
        row = cur.fetchone()
        if row:
            logger.debug(f"チャンク取得成功: ID「{chunk_id}」")
            return dict(row)
        else:
            logger.warning(f"チャンクが見つかりません: ID「{chunk_id}」")
            return None
    except sqlite3.Error as e:
        logger.error(f"チャンク取得エラー: {e}")
        raise
    finally:
        conn.close()


def get_document_list() -> List[Dict]:
    """
    Get a list of all documents ordered by creation date (newest first).
    
    Returns:
        List[Dict]: List of dictionaries containing document metadata
    """
    logger.info("全ドキュメントリストの取得")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM documents ORDER BY created_at DESC")
        rows = cur.fetchall()
        doc_list = [dict(row) for row in rows]
        logger.debug(f"{len(doc_list)}件のドキュメントを取得")
        return doc_list
    except sqlite3.Error as e:
        logger.error(f"ドキュメント一覧取得エラー: {e}")
        raise
    finally:
        conn.close()


def get_chunks_by_document_id(document_id: str) -> List[Dict]:
    """
    Retrieve all chunks belonging to a specific document.
    
    Args:
        document_id (str): ID of the document to retrieve chunks from
        
    Returns:
        List[Dict]: List of dictionaries containing chunk data, ordered by position
    """
    logger.info(f"ドキュメントのチャンク一覧取得: ID「{document_id}」")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY position ASC", (document_id,))
        rows = cur.fetchall()
        chunk_list = [dict(row) for row in rows]
        logger.debug(f"{len(chunk_list)}件のチャンクを取得: ドキュメントID「{document_id}」")
        return chunk_list
    except sqlite3.Error as e:
        logger.error(f"チャンク一覧取得エラー: {e}")
        raise
    finally:
        conn.close()


def delete_document(document_id: str) -> None:
    """
    Delete a document and all its associated chunks.
    
    Args:
        document_id (str): ID of the document to delete
        
    Returns:
        None
    """
    logger.info(f"ドキュメント削除: ID「{document_id}」")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        # チャンク数を取得して記録
        cur.execute("SELECT COUNT(*) FROM chunks WHERE document_id = ?", (document_id,))
        chunk_count = cur.fetchone()[0]
        logger.debug(f"削除対象チャンク数: {chunk_count}件")
        
        # チャンクの削除
        cur.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
        
        # ドキュメントの削除
        cur.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
        
        conn.commit()
        logger.info(f"ドキュメント削除完了: ID「{document_id}」、{chunk_count}件のチャンクを削除")
    except sqlite3.Error as e:
        logger.error(f"ドキュメント削除エラー: {e}")
        raise
    finally:
        conn.close()


def document_exists(document_id: str) -> bool:
    """
    Check if a document with the given ID exists in the database.
    
    Args:
        document_id (str): ID of the document to check
        
    Returns:
        bool: True if document exists, False otherwise
    """
    logger.debug(f"ドキュメント存在確認: ID「{document_id}」")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM documents WHERE document_id = ? LIMIT 1", (document_id,))
        result = cur.fetchone()
        exists = result is not None
        logger.debug(f"ドキュメント存在確認結果: ID「{document_id}」、存在={exists}")
        return exists
    except sqlite3.Error as e:
        logger.error(f"ドキュメント存在確認エラー: {e}")
        raise
    finally:
        conn.close()
