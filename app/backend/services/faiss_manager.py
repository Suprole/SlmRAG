import os
import json
import faiss
import numpy as np
from .logger import Logger
from . import memory_store

# ロガーの初期化
logger = Logger(name="faiss_manager")

FAISS_DIR = "data/faiss"


def get_index_path(document_id: str) -> str:
    return os.path.join(FAISS_DIR, f"{document_id}.index")


def get_meta_path(document_id: str) -> str:
    return os.path.join(FAISS_DIR, f"{document_id}.index.meta")


def create_index(document_id: str, embeddings: list[dict]) -> None:
    """
    チャンクのベクトルをFAISSに登録し、インデックスを保存する。

    Args:
        document_id (str): 対象文書のID
        embeddings (list): 各チャンクの {'chunk_id', 'vector'} を含む辞書のリスト
    """
    logger.info(f"インデックス作成開始: ドキュメントID「{document_id}」、チャンク数: {len(embeddings)}")
    
    vectors = np.array([e["vector"] for e in embeddings], dtype="float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    logger.debug(f"FAISSインデックスに {vectors.shape[0]} ベクトル（次元: {vectors.shape[1]}）を追加")

    chunk_ids = [e["chunk_id"] for e in embeddings]
    
    # Use memory store for Hugging Face Space
    memory_store.store_faiss_index(document_id, index, chunk_ids)
    
    logger.info(f"インデックス作成完了: ドキュメントID「{document_id}」")


def load_index(document_id: str) -> tuple[faiss.Index, list[str]]:
    """
    インデックスとchunk_idリストを読み込む。

    Args:
        document_id (str): 文書ID

    Returns:
        tuple: (FAISSインデックス, chunk_idリスト)
    """
    logger.info(f"インデックス読み込み開始: ドキュメントID「{document_id}」")
    
    # Try loading from memory store first
    result = memory_store.get_faiss_index(document_id)
    
    if result is not None:
        index, chunk_ids = result
        logger.debug(f"メモリからFAISSインデックスを読み込み、チャンク数: {len(chunk_ids)}")
        return index, chunk_ids
    
    # If not in memory or not on HF Spaces, load from file
    index_path = get_index_path(document_id)
    index = faiss.read_index(index_path)
    logger.debug(f"FAISSインデックスを読み込み: {index_path}")
    
    meta_path = get_meta_path(document_id)
    with open(meta_path, "r", encoding="utf-8") as f:
        chunk_ids = json.load(f)
    logger.debug(f"メタデータを読み込み: {meta_path}、チャンク数: {len(chunk_ids)}")
    
    logger.info(f"インデックス読み込み完了: ドキュメントID「{document_id}」")
    return index, chunk_ids


def delete_index(document_id: str) -> None:
    """
    ドキュメントのインデックスとメタデータを削除する。
    
    Args:
        document_id (str): 削除対象の文書ID
    """
    logger.info(f"インデックス削除開始: ドキュメントID「{document_id}」")
    
    # Delete from memory store first
    memory_store.delete_document_data(document_id)
    
    # If not on HF Spaces, also delete from file system
    if not memory_store.is_huggingface_space():
        index_path = get_index_path(document_id)
        meta_path = get_meta_path(document_id)
        
        try:
            if os.path.exists(index_path):
                os.remove(index_path)
                logger.debug(f"インデックスファイルを削除: {index_path}")
            
            if os.path.exists(meta_path):
                os.remove(meta_path)
                logger.debug(f"メタデータファイルを削除: {meta_path}")
        except Exception as e:
            logger.error(f"ファイル削除中にエラー: {e}")
    
    logger.info(f"インデックス削除完了: ドキュメントID「{document_id}」")
