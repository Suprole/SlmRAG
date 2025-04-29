#!/usr/bin/env sh

# 環境変数の設定（適宜変更してください）
HF_USERNAME="onepi"  # Hugging Faceのユーザー名
APP_NAME="SLMRagChat"       # アプリケーション名

# エラーが発生したら終了
set -e

echo "=== Hugging Face RAG Chat デプロイスクリプト ==="

# 1. Hugging Face CLIにログイン
echo "Hugging Face CLIにログインしています..."
if ! command -v huggingface-cli &> /dev/null; then
  echo "Hugging Face CLIがインストールされていません。インストールします..."
  pip install huggingface_hub
fi
huggingface-cli login

# 2. Hugging Face Spaces用のリポジトリを作成（存在しない場合）
echo "Hugging Face Spaceリポジトリを作成します..."
huggingface-cli repo create $APP_NAME --type space --space-sdk docker || echo "リポジトリが既に存在します"

# 3. リポジトリをクローン
echo "リポジトリをクローンします..."
if [ ! -d "$APP_NAME" ]; then
  git clone https://huggingface.co/spaces/$HF_USERNAME/$APP_NAME
else
  echo "ディレクトリ $APP_NAME は既に存在します"
  cd $APP_NAME && git pull && cd ..
fi

# 4. Dockerfileをコピー
echo "Dockerfileをコピーします..."
cp Dockerfile.space $APP_NAME/Dockerfile

# 4.5. アプリケーションコードをコピー
echo "アプリケーションコードをコピーします..."
mkdir -p $APP_NAME/app
cp -r app/backend $APP_NAME/app

# 5. 必要に応じてREADMEを作成
echo "READMEを作成します..."
cat > $APP_NAME/README.md <<'EOL'
---
title: SLM RAG Chat
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
---

# RAG チャットアプリケーション - Hugging Face Space

PDF文書に対して質問応答が可能なチャットアプリケーションです。

## 機能

- PDF ファイルのアップロードと解析
- ドキュメントに基づいた質問応答
- リアルタイムチャットインターフェース
- レスポンシブデザイン

## 技術スタック

- FastAPI (バックエンド)
- LangChain + FAISS (情報検索)
- TinySwallow-1.5B (ローカル言語モデル)

詳細は[GitHub リポジトリ](https://github.com/your-username/ragchat)を参照してください。
EOL

# 6. 変更をコミットしてプッシュ
echo "変更をコミットしてプッシュします..."
cd $APP_NAME
git add Dockerfile README.md
git commit -m "Update Dockerfile and README for Hugging Face Spaces"
git push --force

echo "=== デプロイ完了 ==="
echo "Hugging Face Spacesでビルドが開始されます。以下のURLでアプリケーションにアクセスできます："
echo "https://huggingface.co/spaces/$HF_USERNAME/$APP_NAME" 