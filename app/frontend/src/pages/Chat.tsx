// Chat.tsx

import React, { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getChunks } from "../api/docs";
import { postChat } from "../api/chat";
import { Chunk, ChatMessage } from "../types";
import SidePanel from "../components/SidePanel";

const Chat: React.FC = () => {
  const { documentId } = useParams();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chunks, setChunks] = useState<Chunk[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [highlightedChunkId, setHighlightedChunkId] = useState<string | null>(null);
  const messageEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (documentId) {
      getChunks(documentId).then(setChunks);
    }
  }, [documentId]);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || !documentId) return;
    
    const userMessage: ChatMessage = { role: "user", content: query };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    const assistantMessage: ChatMessage = {
      role: "assistant",
      content: "",
      citations: [],
    };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      await postChat(documentId, query, (chunk) => {
        setMessages((prev) => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          lastMessage.content = chunk.answer;
          lastMessage.citations = chunk.citations;
          return [...newMessages];
        });
      });
    } catch (error) {
      console.error("Error in chat:", error);
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        lastMessage.content = "すみません、エラーが発生しました。もう一度お試しください。";
        return [...newMessages];
      });
    } finally {
      setIsLoading(false);
      setQuery("");
    }
  };

  const handleCitationClick = (chunkId: string) => {
    setHighlightedChunkId(chunkId);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex h-[calc(100vh-8rem)]">
      <div className="w-2/3 flex flex-col bg-white rounded-lg shadow-card overflow-hidden">
        <div className="flex-1 p-6 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center p-6">
              <svg 
                className="w-16 h-16 text-primary-300 mb-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={1.5} 
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" 
                />
              </svg>
              <h3 className="text-xl font-semibold text-secondary-700 mb-2">会話を始めましょう</h3>
              <p className="text-secondary-500 max-w-md">
                このPDFの内容について質問してください。引用付きの回答が得られます。
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <div 
                  key={i} 
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div 
                    className={`max-w-3xl rounded-2xl px-4 py-3 ${
                      msg.role === "user" 
                        ? "bg-primary-600 text-white" 
                        : "bg-secondary-100 text-secondary-900"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-secondary-200 flex flex-wrap gap-1">
                        <span className="text-xs font-medium mr-1">引用:</span>
                        {msg.citations.map((c, idx) => (
                          <button
                            key={idx}
                            className="text-xs px-1.5 py-0.5 rounded bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors"
                            onClick={() => handleCitationClick(c.chunk_id)}
                          >
                            [{idx + 1}]
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              <div ref={messageEndRef} />
            </div>
          )}
        </div>

        <div className="border-t border-secondary-200 p-4">
          <form onSubmit={handleSubmit} className="flex items-end space-x-2">
            <div className="flex-1 relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full p-3 pr-10 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
                rows={2}
                placeholder="質問を入力してください..."
                disabled={isLoading}
              ></textarea>
              <span className="absolute right-2 bottom-2 text-xs text-secondary-400">
                Enterで送信、Shift+Enterで改行
              </span>
            </div>
            <button
              type="submit"
              disabled={!query.trim() || isLoading}
              className={`p-3 rounded-lg ${
                !query.trim() || isLoading
                  ? "bg-secondary-300 cursor-not-allowed"
                  : "bg-primary-600 hover:bg-primary-700 text-white transition-colors"
              }`}
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              )}
            </button>
          </form>
        </div>
      </div>

      <SidePanel
        documentId={documentId!}
        chunks={chunks}
        highlightedChunkId={highlightedChunkId}
      />
    </div>
  );
};

export default Chat;