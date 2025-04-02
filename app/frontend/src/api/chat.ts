const API_URL = "http://localhost:8000/api";

export async function postChat(documentId: string, query: string): Promise<{
  answer: string;
  citations: {
    chunk_id: string;
    text: string;
    chapter: string;
  }[];
}> {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ document_id: documentId, query }),
  });

  if (!res.ok) {
    throw new Error("Failed to get chat response");
  }

  return res.json();
}
