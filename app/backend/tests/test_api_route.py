import os
import shutil
import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from services import models

client = TestClient(app)

SAMPLE_PDF_PATH = r"C:\Users\diosc\M1\Job\Suprole\projects\ragChat\app\backend\tests\インターネット公開型情報システム開発・運用標準_20241201改正 (1).pdf"

# Declare uploaded_doc at the module level
uploaded_doc = None

def setup_module(module):
    # 環境初期化
    shutil.rmtree("data/db", ignore_errors=True)
    shutil.rmtree("data/faiss", ignore_errors=True)
    shutil.rmtree("data/markdown", ignore_errors=True)
    os.makedirs("data/db", exist_ok=True)
    os.makedirs("data/faiss", exist_ok=True)
    os.makedirs("data/markdown", exist_ok=True)
    models.init_db()

def test_01_upload_pdf():
    global uploaded_doc
    
    # Check if the PDF file exists
    if not os.path.exists(SAMPLE_PDF_PATH):
        pytest.fail(f"PDF file not found at: {SAMPLE_PDF_PATH}")
    
    try:
        with open(SAMPLE_PDF_PATH, "rb") as f:
            response = client.post("/api/upload", files={"file": ("sample.pdf", f, "application/pdf")})
        
        # Print response details for debugging if it fails
        if response.status_code != 200:
            print(f"API Error: Status Code {response.status_code}")
            print(f"Response text: {response.text}")
            pytest.fail(f"Upload failed with status code {response.status_code}")
        
        assert response.status_code == 200
        uploaded_doc = response.json()
        assert "document_id" in uploaded_doc
    except Exception as e:
        print(f"Exception during upload: {str(e)}")
        pytest.fail(f"Exception: {str(e)}")


def test_02_list_documents():
    response = client.get("/api/docs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_03_get_chunks():
    if uploaded_doc is None:
        pytest.skip("Skipping test as document upload failed")
    
    doc_id = uploaded_doc["document_id"]
    response = client.get(f"/api/docs/{doc_id}/chunks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_04_get_markdown():
    if uploaded_doc is None:
        pytest.skip("Skipping test as document upload failed")
    
    doc_id = uploaded_doc["document_id"]
    response = client.get(f"/api/docs/{doc_id}/markdown")
    assert response.status_code == 200
    assert "markdown" in response.json()


def test_05_chat():
    if uploaded_doc is None:
        pytest.skip("Skipping test as document upload failed")
    
    doc_id = uploaded_doc["document_id"]
    response = client.post("/api/chat", json={"document_id": doc_id, "query": "この文書の目的は？"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["citations"], list)


def test_06_delete_document():
    if uploaded_doc is None:
        pytest.skip("Skipping test as document upload failed")
    
    doc_id = uploaded_doc["document_id"]
    response = client.delete(f"/api/docs/{doc_id}")
    assert response.status_code == 200
    assert "deleted" in response.json().get("message", "")
