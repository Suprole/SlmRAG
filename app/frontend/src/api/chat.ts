const API_URL = "http://localhost:8000/api";

export async function postChat(
  documentId: string,
  query: string,
  onChunk: (chunk: { answer: string; citations: any[] }) => void
): Promise<void> {
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

  const reader = res.body?.getReader();
  if (!reader) {
    throw new Error("Failed to get response reader");
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = new TextDecoder().decode(value);
    const data = JSON.parse(chunk);
    onChunk(data);
  }
}
