# RAG Chat

PDF ファイルをアップロードし、AI と対話するための RAG（Retrieval Augmented Generation）チャットアプリケーションです。

## 特徴

- PDF のアップロードと自動処理
- PDF コンテンツに関する質問応答
- 引用付きの回答
- 元のドキュメントでの引用箇所のハイライト表示
- CPU runtime でも高速な応答

## アーキテクチャ

- フロントエンド: React, TypeScript, Tailwind CSS
- バックエンド: FastAPI
- ベクトル検索: FAISS
- テキスト埋め込み: Sentence Transformers
- 生成 AI: llama-cpp-python (Tiny Swallow)

## Hugging Face Spaces へのデプロイ

このアプリケーションは Hugging Face Spaces にデプロイできます。

### 1. Hugging Face Space の作成

1. Hugging Face にログインし、[New Space](https://huggingface.co/new-space) を作成
2. Space の名前を設定（例: `ragchat`）
3. SDK として「Docker」を選択
4. Space を作成

### 2. GitHub リポジトリの準備

#### GitHub Secrets の設定

GitHub の Settings > Secrets and Variables > Actions で以下の Secrets を設定します：

- `HF_TOKEN`: Hugging Face の API トークン（書き込み権限付き）
- `HF_USERNAME`: Hugging Face のユーザー名
- `SPACE_NAME`: 作成した Space の名前（例: `ragchat`）

### 3. GitHub Actions による自動デプロイ

リポジトリの `main` ブランチに変更をプッシュすると、GitHub Actions が自動的に Hugging Face Space にデプロイします。

## 注意点

- このデプロイ方法では、PDF と生成されたベクトルインデックスはメモリに保存され、永続化されません。アプリケーションを再起動すると、アップロードされたすべてのドキュメントは失われます。
- CPU ランタイムを想定しているため、大量のドキュメントや大きなモデルには適していません。

## ローカル開発環境のセットアップ

### バックエンド

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### フロントエンド

```bash
cd app/frontend
npm install
npm run dev
```
