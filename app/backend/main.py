from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api import upload, chat, docs
from services import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.init_db()  # ✅ 起動時に DB を初期化
    yield  # アプリケーションが動いている間
    # 終了時に何か処理したければここに書ける

app = FastAPI(
    title="RAGチャットAPI",
    version="0.1.0",
    lifespan=lifespan
)

# ✅ CORSミドルウェア設定（ローカル開発用に緩め）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーティング登録
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(docs.router, prefix="/api")
