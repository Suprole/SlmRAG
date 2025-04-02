// SidePanel.tsx

import React, { useEffect, useRef, useState } from "react";
import { Chunk } from "../types";

type Props = {
  documentId: string;
  chunks: Chunk[];
  highlightedChunkId: string | null;
};

const SidePanel: React.FC<Props> = ({ documentId, chunks, highlightedChunkId }) => {
  const chunkRefs = useRef<Map<string, HTMLDivElement>>(new Map());
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(new Set());
  
  // チャプターごとにチャンクをグループ化
  const chapterGroups = React.useMemo(() => {
    const groups: Record<string, Chunk[]> = {};
    chunks.forEach(chunk => {
      const chapter = chunk.chapter || "その他";
      if (!groups[chapter]) {
        groups[chapter] = [];
      }
      groups[chapter].push(chunk);
    });
    return groups;
  }, [chunks]);

  useEffect(() => {
    if (highlightedChunkId) {
      const ref = chunkRefs.current.get(highlightedChunkId);
      if (ref) {
        ref.scrollIntoView({ behavior: "smooth", block: "center" });
        ref.classList.add("bg-primary-100");
        setTimeout(() => {
          ref.classList.remove("bg-primary-100");
        }, 2000);
      }
    }
  }, [highlightedChunkId]);

  // チャプターの展開・折りたたみを切り替え
  const toggleChapter = (chapter: string) => {
    const newExpanded = new Set(expandedChapters);
    if (newExpanded.has(chapter)) {
      newExpanded.delete(chapter);
    } else {
      newExpanded.add(chapter);
    }
    setExpandedChapters(newExpanded);
  };

  // ハイライトされたチャンクのチャプターを自動展開
  useEffect(() => {
    if (highlightedChunkId) {
      const highlightedChunk = chunks.find(c => c.chunk_id === highlightedChunkId);
      if (highlightedChunk && highlightedChunk.chapter) {
        setExpandedChapters(prev => new Set(prev).add(highlightedChunk.chapter));
      }
    }
  }, [highlightedChunkId, chunks]);

  // 検索に基づいてチャンクをフィルタリング
  const filteredChapters = React.useMemo(() => {
    if (!searchTerm.trim()) return Object.keys(chapterGroups);
    
    const results: string[] = [];
    Object.entries(chapterGroups).forEach(([chapter, chunkList]) => {
      const hasMatch = chunkList.some(chunk => 
        chunk.text.toLowerCase().includes(searchTerm.toLowerCase())
      );
      if (hasMatch) results.push(chapter);
    });
    return results;
  }, [chapterGroups, searchTerm]);

  const filteredChunks = React.useCallback((chapter: string) => {
    if (!searchTerm.trim()) return chapterGroups[chapter];
    
    return chapterGroups[chapter].filter(chunk => 
      chunk.text.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [chapterGroups, searchTerm]);

  return (
    <div className="w-1/3 h-full flex flex-col border-l border-secondary-200 bg-white">
      <div className="py-3 px-4 border-b border-secondary-200 flex items-center justify-between">
        <h2 className="text-lg font-medium text-secondary-900">ドキュメント内容</h2>
        <div className="relative w-48">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="検索..."
            className="w-full pl-8 pr-3 py-1 text-sm rounded-md border border-secondary-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
          <svg
            className="absolute left-2.5 top-1.5 h-4 w-4 text-secondary-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {filteredChapters.length === 0 ? (
          <div className="py-6 text-center text-secondary-500">
            <p>検索結果がありません</p>
          </div>
        ) : (
          filteredChapters.map((chapter) => (
            <div key={chapter} className="border-b border-secondary-100">
              <button
                onClick={() => toggleChapter(chapter)}
                className="w-full px-4 py-2 flex items-center justify-between hover:bg-secondary-50 transition-colors"
              >
                <span className="font-medium text-secondary-800">{chapter}</span>
                <svg
                  className={`w-5 h-5 text-secondary-500 transition-transform duration-200 ${
                    expandedChapters.has(chapter) ? "transform rotate-180" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {expandedChapters.has(chapter) && (
                <div className="bg-secondary-50 border-t border-secondary-100">
                  {filteredChunks(chapter).map((chunk) => (
                    <div
                      key={chunk.chunk_id}
                      ref={(el) => {
                        if (el) chunkRefs.current.set(chunk.chunk_id, el);
                      }}
                      className={`px-4 py-3 border-b border-secondary-100 last:border-b-0 text-sm transition-colors duration-150 ${
                        highlightedChunkId === chunk.chunk_id
                          ? "bg-primary-100"
                          : "hover:bg-secondary-100"
                      }`}
                    >
                      <p className="text-secondary-800 whitespace-pre-wrap">{chunk.text}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SidePanel;