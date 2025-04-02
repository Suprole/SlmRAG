from llama_cpp import Llama
from typing import List, Dict, Tuple
import os

MODEL_PATH = os.path.join("models", "tinyswallow-1.5b-instruct-q8_0.gguf")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    use_mlock=True
)

# slmのwarm start
llm("こんにちは。", max_tokens=0)

def build_prompt(query: str, chunks: List[Dict]) -> str:
    """
    Qwenベースモデル向けのChatML風プロンプトを構築する。

    Args:
        query (str): 質問
        chunks (list): 検索で得たチャンクリスト

    Returns:
        str: LLMに渡すプロンプト
    """
    system_prompt = "あなたは誠実で優秀なアシスタントです。"

    references = "\n".join(
        f"[{i + 1}] {chunk['text'].strip()}" for i, chunk in enumerate(chunks)
    )

    user_prompt = (
        f"質問: {query}\n"
        "参考情報:\n"
        f"{references}"
    )

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
    prompt = build_prompt(query, chunks)

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

    return answer, citations
