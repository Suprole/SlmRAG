from sentence_transformers import SentenceTransformer
from typing import List

# 軽量＆高精度な汎用モデル（推奨）
MODEL_NAME = "all-MiniLM-L6-v2"

# モデルの初期化（warm start前提）
_model = SentenceTransformer(MODEL_NAME)


def vectorize_text(text: str) -> List[float]:
    """
    チャンク化されたテキストをベクトルに変換する。

    Args:
        text (str): 1チャンクの本文テキスト

    Returns:
        List[float]: 正規化済みベクトル（384次元）
    """
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
