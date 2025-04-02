# RAG チャットアプリケーション

PDF 文書に対して質問応答が可能なチャットアプリケーションです。アプリケーションは React フロントエンドと Python バックエンドで構成されています。

## 機能

- PDF ファイルのアップロードと解析
- ドキュメントに基づいた質問応答
- リアルタイムチャットインターフェース
- レスポンシブデザイン

## 必要要件

### バックエンド

- Python 3.9 以上
- pip (Python パッケージマネージャー)

### フロントエンド

- Node.js 18.0.0 以上
- npm 9.0.0 以上

## セットアップ手順

### バックエンドのセットアップ

0. 以下のディレクトリを作成します：

```bash
mkdir -p app/backend/data/db
mkdir -p app/backend/data/faiss
mkdir -p app/backend/data/markdown
```


1. バックエンドディレクトリに移動します：

```bash
cd app/backend
```

2. Python 仮想環境を作成し、有効化します：

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

4. バックエンドサーバーを起動します：

```bash
uvicorn main:app --reload --port 8000
```

### 言語モデルのセットアップ

1. backend/models ディレクトリが存在することを確認します。存在しない場合は作成します：

```bash
mkdir -p app/backend/models
```

2. Hugging Face から TinySwallow-1.5B モデルをダウンロードします：
   - [TinySwallow-1.5B-Instruct-GGUF](https://huggingface.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF?show_file_info=tinyswallow-1.5b-instruct-q8_0.gguf) にアクセスします
   - `tinyswallow-1.5b-instruct-q8_0.gguf` ファイルをダウンロードします
   - ダウンロードしたファイルを `app/backend/models` ディレクトリに配置します

### フロントエンドのセットアップ

1. 新しいターミナルを開き、フロントエンドディレクトリに移動します：

```bash
cd app/frontend
```

2. 依存パッケージをインストールします：

```bash
npm install
```

3. 開発サーバーを起動します：

```bash
npm run dev
```

## 使用方法

1. ブラウザで http://localhost:5173 にアクセスします
2. サイドパネルから PDF ファイルをアップロードします
3. アップロードしたドキュメントに関する質問を入力します
4. AI アシスタントが文書の内容に基づいて回答を生成します

## 技術スタック

### フロントエンド

- React 19.0
- TypeScript
- Vite
- TailwindCSS
- React Router

### バックエンド

- FastAPI
- LangChain
- FAISS（ベクトル検索）
- Sentence Transformers
- TinySwallow-1.5B (ローカル言語モデル)
