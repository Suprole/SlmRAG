import { useEffect, useState} from "react";
import { useParams } from "react-router-dom";
import { getChunks, getMarkdown } from "../api/docs";
import { postChat } from "../api/chat";
import type { Chunk, Citation } from "../types";
import SidePanel from "../components/SidePanel";

export default function Chat() {
  const { documentId } = useParams();
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [markdown, setMarkdown] = useState("");
  const [chunks, setChunks] = useState<Chunk[]>([]);

  useEffect(() => {
    if (documentId) {
      getMarkdown(documentId).then(setMarkdown);
      getChunks(documentId).then(setChunks);
    }
  }, [documentId]);

  const handleSend = async () => {
    const res = await postChat(documentId!, query);
    setAnswer(res.answer);
    setCitations(res.citations);
  };

  const handleCitationClick = (chunkId: string) => {
    const el = document.getElementById(chunkId);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      el.classList.add("bg-yellow-100");
      setTimeout(() => el.classList.remove("bg-yellow-100"), 2000);
    }
  };

  return (
    <div className="grid grid-cols-2 h-screen">
      <div className="p-6 flex flex-col">
        <h1 className="text-xl font-bold mb-4">💬 質問</h1>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 w-full h-32 mb-2"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          送信
        </button>
        <div className="mt-6">
          <h2 className="font-semibold">回答</h2>
          <p className="whitespace-pre-wrap mt-2">{answer}</p>
          <div className="mt-2 space-x-2">
            {citations.map((c, i) => (
              <button
                key={i}
                onClick={() => handleCitationClick(c.chunk_id)}
                className="text-sm text-blue-600 underline"
              >
                [{i + 1}]
              </button>
            ))}
          </div>
        </div>
      </div>
      <SidePanel markdown={markdown} chunks={chunks} />
    </div>
  );
}