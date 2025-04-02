from llama_cpp import Llama
from typing import List, Dict, Tuple
import os
from .logger import Logger

MODEL_PATH = os.path.join("models", "tinyswallow-1.5b-instruct-q8_0.gguf")

# ロガーの初期化
logger = Logger(name="generator")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    use_mlock=True
)

# slmのwarm start
logger.info("LLMモデルをウォームアップしています")
llm("こんにちは。", max_tokens=0)
# ストリーミングモードでも初期化しておく
logger.info("LLMモデルをストリーミングモードでウォームアップしています")
for _ in llm("こんにちは。", max_tokens=1, stream=True):
    pass
logger.info("LLMモデルのウォームアップが完了しました")

def build_prompt(query: str, chunks: List[Dict]) -> str:
    """
    Qwenベースモデル向けのChatML風プロンプトを構築する。
    マークダウン形式を使いAIフレンドリーな構造化フォーマットで出力。

    Args:
        query (str): 質問
        chunks (list): 検索で得たチャンクリスト

    Returns:
        str: LLMに渡すプロンプト
    """
    logger.debug(f"プロンプト構築開始: 質問「{query}」、チャンク数: {len(chunks)}")
    system_prompt = """# アシスタント設定
あなたは誠実で優秀なアシスタントです。以下のガイドラインに従って回答を作成してください。

## 回答のルール
- 提供された参考情報のみに基づいて回答してください
- 参考情報に含まれていない内容については「参考情報にはその点について記載がありません」と正直に伝えてください
- 想像や推測で回答を作らないでください
- 参考情報の番号[1]、[2]などを使って引用元を明示してください
- 簡潔かつ明確な回答を心がけてください

## 出力形式
- マークダウン記法を使用して回答を構造化してください
- 見出し（#, ##）、箇条書き（- または1.）、太字（**強調**）などを適切に使用してください
- コードブロックは ``` で囲んでください
- 表が必要な場合はマークダウン形式の表を使用してください
"""

    # 参考情報を構造化して表示
    formatted_references = ""
    for i, chunk in enumerate(chunks):
        formatted_references += f"### 参考資料[{i + 1}]\n{chunk['text'].strip()}\n\n"

    user_prompt = f"""# 質問
{query}

# 参考情報
{formatted_references}

## 指示
上記の参考情報のみを使って回答を作成してください。参考情報に含まれていない内容については回答せず、「参考情報にはその点について記載がありません」と伝えてください。必ず参考情報の番号[1]、[2]などを引用として使用してください。
"""

    prompt = (
        "<|im_start|>system\n"
        f"{system_prompt}\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{user_prompt}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    # debug: print(prompt)
    print(prompt)
    logger.debug("プロンプト構築完了")
    return prompt


def generate_answer(query: str, chunks: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    チャット用プロンプトを構築してLLMで回答を生成。

    Args:
        query (str): 質問内容
        chunks (list): 関連チャンクのリスト

    Returns:
        tuple: (回答テキスト, 引用情報リスト)
    """
    logger.info(f"回答生成開始: 質問「{query}」、チャンク数: {len(chunks)}")
    prompt = build_prompt(query, chunks)

    logger.debug("LLMへのリクエスト送信")
    output = llm(
        prompt=prompt,
        max_tokens=512,
        stop=["<|im_end|>"],
        echo=False,
        stream=True
    )

    answer = ""
    for chunk in output:
        if chunk["choices"][0]["text"]:
            answer += chunk["choices"][0]["text"]

    citations = [
        {
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "reference": f"[{i + 1}]"
        }
        for i, chunk in enumerate(chunks)
    ]

    logger.info(f"回答生成完了: 回答文字数 {len(answer)}")
    return answer, citations

def generate_answer_stream(query: str, chunks: List[Dict]):
    """
    ストリーミングモードでLLMからの回答を生成するジェネレータ関数。
    トークンごとに返すことでフロントエンドでのUXを向上させる。

    Args:
        query (str): 質問内容
        chunks (list): 関連チャンクのリスト

    Yields:
        str: 生成されたトークン
    """
    logger.info(f"ストリーミング回答生成開始: 質問「{query}」、チャンク数: {len(chunks)}")
    prompt = build_prompt(query, chunks)

    logger.debug("LLMへのストリーミングリクエスト送信")
    output = llm(
        prompt=prompt,
        max_tokens=512,
        stop=["<|im_end|>"],
        echo=False,
        stream=True
    )

    for chunk in output:
        token = chunk["choices"][0]["text"]
        if token:
            logger.debug(f"トークン生成: {token}")
            yield token

    logger.info("ストリーミング回答生成完了")
