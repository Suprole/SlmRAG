import { Chunk } from "../types/index";

const API_URL = "http://localhost:8000/api";

export async function uploadPdf(file: File): Promise<{ document_id: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  return res.json();
}

export async function getDocuments(): Promise<{ document_id: string; title: string }[]> {
  const res = await fetch(`${API_URL}/docs`);
  if (!res.ok) {
    throw new Error("Failed to fetch documents");
  }
  return res.json();
}

export async function getMarkdown(documentId: string): Promise<string> {
  const res = await fetch(`${API_URL}/docs/${documentId}/markdown`);
  if (!res.ok) {
    throw new Error("Failed to fetch markdown");
  }
  const data = await res.json();
  return data.markdown;
} 

export async function getChunks(documentId: string): Promise<Chunk[]> {
  const res = await fetch(`${API_URL}/docs/${documentId}/chunks`);
  if (!res.ok) {
    throw new Error("Failed to fetch chunks");
  }
  return res.json();
}

export async function deleteDocument(documentId: string): Promise<void> {
  const res = await fetch(`${API_URL}/docs/${documentId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error("Failed to delete document");
  }
}
