# RAG チャットアプリケーション

PDF文書に対して質問応答が可能なチャットアプリケーションです。アプリケーションはReactフロントエンドとPythonバックエンドで構成されています。

## 機能

- PDFファイルのアップロードと解析
- ドキュメントに基づいた質問応答
- リアルタイムチャットインターフェース
- レスポンシブデザイン

## 必要要件

### バックエンド
- Python 3.9以上
- pip (Pythonパッケージマネージャー)

### フロントエンド
- Node.js 18.0.0以上
- npm 9.0.0以上

## セットアップ手順

### バックエンドのセットアップ

1. バックエンドディレクトリに移動します：
```bash
cd app/backend
```

2. Python仮想環境を作成し、有効化します：
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
2. サイドパネルからPDFファイルをアップロードします
3. アップロードしたドキュメントに関する質問を入力します
4. AIアシスタントが文書の内容に基づいて回答を生成します

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
