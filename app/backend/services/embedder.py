from sentence_transformers import SentenceTransformer
from typing import List
from .logger import Logger

# ロガーの初期化
logger = Logger(name="embedder")

# 軽量＆高精度な汎用モデル（推奨）
MODEL_NAME = "pkshatech/GLuCoSE-base-ja-v2"

# モデルの初期化（warm start前提）
logger.info(f"埋め込みモデル「{MODEL_NAME}」の初期化を開始")
_model = SentenceTransformer(MODEL_NAME)
logger.info("埋め込みモデルの初期化が完了しました")


def vectorize_text(text: str) -> List[float]:
    """
    チャンク化されたテキストをベクトルに変換する。

    Args:
        text (str): 1チャンクの本文テキスト

    Returns:
        List[float]: 正規化済みベクトル（384次元）
    """
    logger.debug(f"テキスト（文字数: {len(text)}）のベクトル化を開始")
    embedding = _model.encode(text, normalize_embeddings=True)
    result = embedding.tolist()
    logger.debug(f"ベクトル化完了: 次元数 {len(result)}")
    return result
