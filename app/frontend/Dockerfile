# === ビルドステージ ===
FROM node:18-alpine AS builder

WORKDIR /usr/src/app

# ビルド引数を定義
ARG VITE_API_URL=http://localhost:8000/api

# package.jsonとlockファイルをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm ci

# ソースコードをコピー
COPY . .

# 環境変数を設定
ENV VITE_API_URL=${VITE_API_URL}

# アプリケーションをビルド
RUN npm run build

# === サーブステージ ===
FROM nginx:alpine

# ビルドステージからビルド成果物をコピー
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

# カスタムNginx設定をコピー
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ポートを公開
EXPOSE 80

# Nginxをフォアグラウンドで実行
CMD ["nginx", "-g", "daemon off;"] 