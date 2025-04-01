import sqlite3
import os
from typing import Optional, Dict, List
from datetime import datetime

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
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        );
    """)
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
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (document_id, title, created_at) VALUES (?, ?, ?)",
        (document_id, title, created_at.isoformat())
    )
    conn.commit()
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
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chunks (chunk_id, document_id, chapter, position, text) VALUES (?, ?, ?, ?, ?)",
        (chunk_id, document_id, chapter, position, text)
    )
    conn.commit()
    conn.close()


def get_chunk_by_id(chunk_id: str) -> Optional[Dict]:
    """
    Retrieve a specific chunk by its ID.
    
    Args:
        chunk_id (str): ID of the chunk to retrieve
        
    Returns:
        Optional[Dict]: Dictionary containing chunk data if found, None otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM chunks WHERE chunk_id = ?", (chunk_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_document_list() -> List[Dict]:
    """
    Get a list of all documents ordered by creation date (newest first).
    
    Returns:
        List[Dict]: List of dictionaries containing document metadata
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_chunks_by_document_id(document_id: str) -> List[Dict]:
    """
    Retrieve all chunks belonging to a specific document.
    
    Args:
        document_id (str): ID of the document to retrieve chunks from
        
    Returns:
        List[Dict]: List of dictionaries containing chunk data, ordered by position
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY position ASC", (document_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_document(document_id: str) -> None:
    """
    Delete a document and all its associated chunks.
    
    Args:
        document_id (str): ID of the document to delete
        
    Returns:
        None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
    cur.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
    conn.commit()
    conn.close()


def document_exists(document_id: str) -> bool:
    """
    Check if a document with the given ID exists in the database.
    
    Args:
        document_id (str): ID of the document to check
        
    Returns:
        bool: True if document exists, False otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM documents WHERE document_id = ? LIMIT 1", (document_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None
