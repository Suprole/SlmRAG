# backend/main.py
from fastapi import FastAPI
from api import upload, chat, docs

app = FastAPI()

# APIルーター登録
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(docs.router, prefix="/api")
