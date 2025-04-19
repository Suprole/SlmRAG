FROM node:22-slim AS frontend-builder

WORKDIR /app/frontend
# Copy frontend files
COPY app/frontend/ ./
# Build frontend
RUN npm install
RUN npm run build

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create in-memory directories
RUN mkdir -p /app/data/markdown /app/data/faiss /app/data/db

# Copy backend requirements
COPY app/backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/backend/ ./

# Copy frontend build from the previous stage
COPY --from=frontend-builder /app/frontend/dist/ ./static/

# Hugging Face - download models at build time
RUN mkdir -p models
# Download models (modify this depending on which model you want to use)
# Using tinyswallow-1.5b-instruct-q5_k_m.gguf and GLuCoSE model
RUN python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='Hugging-Face-Meetups/tinyswallow-1.5b-instruct-gguf', \
    filename='tinyswallow-1.5b-instruct-q5_k_m.gguf', local_dir='models'); \
    from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('pkshatech/GLuCoSE-base-ja-v2');"

# Modify main.py to serve static files
RUN sed -i '/app = FastAPI/,/lifespan=lifespan/c\app = FastAPI(\n    title="RAGチャットAPI",\n    version="0.1.0",\n    lifespan=lifespan\n)\n\nfrom fastapi.staticfiles import StaticFiles\napp.mount("/", StaticFiles(directory="static", html=True), name="static")' main.py

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]