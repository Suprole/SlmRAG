FROM python:3.10-slim

WORKDIR /app

# ビルドに必要なツールをインストール (gitも追加)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 依存関係を先にコピーしてインストール（レイヤーキャッシュを活用）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# データとモデルのディレクトリを作成（docker-composeでマウントするが念のため）
RUN mkdir -p /app/data/db /app/data/faiss /app/data/markdown /app/models

# ポートを公開
EXPOSE 8000

# アプリケーションを実行（0.0.0.0で外部からのアクセスを受け付ける）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 