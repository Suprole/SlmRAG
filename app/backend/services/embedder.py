import numpy as np


def vectorize_text(text: str) -> list[float]:
    """
    テキストをベクトルに変換する。ダミーではランダムなベクトルを返す。

    Args:
        text (str): 入力テキスト

    Returns:
        list[float]: ベクトル（768次元など）
    """
    # TODO: 実際は事前学習済みモデルなどに置き換え
    return np.random.rand(768).astype("float32").tolist()
