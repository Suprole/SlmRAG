import os
import json
import faiss
import numpy as np
from .logger import Logger

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
    
    os.makedirs(FAISS_DIR, exist_ok=True)
    logger.debug(f"インデックスディレクトリ確認: {FAISS_DIR}")

    vectors = np.array([e["vector"] for e in embeddings], dtype="float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    logger.debug(f"FAISSインデックスに {vectors.shape[0]} ベクトル（次元: {vectors.shape[1]}）を追加")

    chunk_ids = [e["chunk_id"] for e in embeddings]
    index_path = get_index_path(document_id)
    faiss.write_index(index, index_path)
    logger.debug(f"インデックスをファイルに保存: {index_path}")

    meta_path = get_meta_path(document_id)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(chunk_ids, f)
    logger.debug(f"メタデータをファイルに保存: {meta_path}")
    
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
    
    index_path = get_index_path(document_id)
    meta_path = get_meta_path(document_id)
    
    os.remove(index_path)
    logger.debug(f"インデックスファイルを削除: {index_path}")
    
    os.remove(meta_path)
    logger.debug(f"メタデータファイルを削除: {meta_path}")
    
    logger.info(f"インデックス削除完了: ドキュメントID「{document_id}」")
