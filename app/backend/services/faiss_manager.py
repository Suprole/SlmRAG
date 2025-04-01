import os
import json
import faiss
import numpy as np

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
    os.makedirs(FAISS_DIR, exist_ok=True)

    vectors = np.array([e["vector"] for e in embeddings], dtype="float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    chunk_ids = [e["chunk_id"] for e in embeddings]
    faiss.write_index(index, get_index_path(document_id))

    with open(get_meta_path(document_id), "w", encoding="utf-8") as f:
        json.dump(chunk_ids, f)


def load_index(document_id: str) -> tuple[faiss.Index, list[str]]:
    """
    インデックスとchunk_idリストを読み込む。

    Args:
        document_id (str): 文書ID

    Returns:
        tuple: (FAISSインデックス, chunk_idリスト)
    """
    index = faiss.read_index(get_index_path(document_id))
    with open(get_meta_path(document_id), "r", encoding="utf-8") as f:
        chunk_ids = json.load(f)
    return index, chunk_ids


def delete_index(document_id: str) -> None:
    os.remove(get_index_path(document_id))
    os.remove(get_meta_path(document_id))
