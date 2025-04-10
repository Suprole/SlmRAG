from services import embedder, faiss_manager
from services.models import get_chunk_by_id  # SQLiteモデル（models.pyに定義されている前提）
import numpy as np
from .logger import Logger

# ロガーの初期化
logger = Logger(name="retriever")


def retrieve_top_chunks(document_id: str, query: str, top_k: int = 2) -> list[dict]:
    """
    クエリをベクトル化し、FAISSでtop_k件の近傍チャンクを検索・取得する。

    Args:
        document_id (str): 検索対象のドキュメントID
        query (str): ユーザーの質問
        top_k (int): 上位何件を取得するか

    Returns:
        list[dict]: チャンクのメタ情報リスト
    """
    logger.info(f"検索開始: ドキュメントID「{document_id}」、クエリ「{query}」、top_k={top_k}")
    
    index, chunk_ids = faiss_manager.load_index(document_id)
    logger.debug(f"インデックスロード完了: チャンク数 {len(chunk_ids)}")
    
    query_vector = np.array([embedder.vectorize_text(query)], dtype="float32")
    logger.debug("クエリベクトル生成完了")
    
    _, indices = index.search(query_vector, top_k)
    
    top_chunk_ids = [chunk_ids[i] for i in indices[0] if i < len(chunk_ids)]
    chunks = [get_chunk_by_id(cid) for cid in top_chunk_ids]
    
    logger.info(f"検索完了: {len(chunks)}件のチャンクを取得")
    return chunks
