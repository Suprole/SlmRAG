// SidePanel.tsx

import React, { useEffect, useRef, useState } from "react";
import { Chunk } from "../types";
import { getMarkdown } from "../api/docs";

type Props = {
  documentId: string;
  chunks: Chunk[];
  highlightedChunkId: string | null;
};

const SidePanel: React.FC<Props> = ({ documentId, chunks, highlightedChunkId }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [markdown, setMarkdown] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const contentRef = useRef<HTMLDivElement>(null);
  const highlightRef = useRef<HTMLSpanElement | null>(null);
  
  // すべてのハイライト済みチャンクIDを追跡
  const [activeHighlightIds, setActiveHighlightIds] = useState<Set<string>>(new Set());

  // マークダウン全文を取得
  useEffect(() => {
    const fetchMarkdown = async () => {
      setLoading(true);
      try {
        const md = await getMarkdown(documentId);
        setMarkdown(md);
      } catch (error) {
        console.error("マークダウンの取得に失敗しました", error);
      } finally {
        setLoading(false);
      }
    };
    
    if (documentId) {
      fetchMarkdown();
      // ドキュメントが変わったら全てのハイライトをクリア
      setActiveHighlightIds(new Set());
    }
  }, [documentId]);

  // 新しいハイライトがある場合、アクティブなハイライトセットに追加
  useEffect(() => {
    if (highlightedChunkId) {
      setActiveHighlightIds(prev => {
        const newSet = new Set(prev);
        newSet.add(highlightedChunkId);
        return newSet;
      });
    }
  }, [highlightedChunkId]);

  // フィルタリングされたマークダウンを取得
  const getFilteredMarkdown = () => {
    if (!markdown) return "";
    
    if (!searchTerm.trim()) return markdown;
    
    return markdown
      .split('\n')
      .filter(line => line.toLowerCase().includes(searchTerm.toLowerCase()))
      .join('\n');
  };

  // アクティブなすべてのチャンクを取得
  const activeChunks = React.useMemo(() => {
    return Array.from(activeHighlightIds)
      .map(id => chunks.find(c => c.chunk_id === id))
      .filter((chunk): chunk is Chunk => chunk !== undefined);
  }, [chunks, activeHighlightIds]);

  // ハイライト済みマークダウンテキストを生成
  const getHighlightedMarkdown = () => {
    if (!markdown || activeChunks.length === 0) {
      return filteredMarkdown;
    }

    let result = filteredMarkdown;
    const highlightedSpans: Array<{ start: number; end: number; chunkId: string }> = [];
    
    // 各チャンクの位置を特定し、重複しないようハイライト対象として記録
    activeChunks.forEach(chunk => {
      let startIndex = 0;
      while (true) {
        const index = result.indexOf(chunk.text, startIndex);
        if (index === -1) break;
        
        // チャンクの位置を記録
        highlightedSpans.push({
          start: index,
          end: index + chunk.text.length,
          chunkId: chunk.chunk_id
        });
        
        startIndex = index + 1;
      }
    });
    
    // ソートして重複部分を統合（終了位置の降順）
    highlightedSpans.sort((a, b) => a.start - b.start);
    const mergedSpans: typeof highlightedSpans = [];
    
    // 重複したスパンを統合
    for (const span of highlightedSpans) {
      if (mergedSpans.length === 0) {
        mergedSpans.push(span);
        continue;
      }
      
      const lastSpan = mergedSpans[mergedSpans.length - 1];
      if (span.start <= lastSpan.end) {
        // スパンが重複している場合、統合
        lastSpan.end = Math.max(lastSpan.end, span.end);
        // 最新のチャンクIDを優先
        if (span.chunkId === highlightedChunkId) {
          lastSpan.chunkId = span.chunkId;
        }
      } else {
        // 重複がなければ追加
        mergedSpans.push(span);
      }
    }
    
    // 後ろから前に処理することで、インデックスの変化を防ぐ
    let highlightedText = result;
    for (let i = mergedSpans.length - 1; i >= 0; i--) {
      const { start, end, chunkId } = mergedSpans[i];
      const text = highlightedText.substring(start, end);
      const isLatest = chunkId === highlightedChunkId;
      
      // ハイライトタグを追加
      const className = isLatest 
        ? "bg-primary-200 px-1 py-0.5 rounded" 
        : "bg-secondary-100 px-1 py-0.5 rounded";
      
      const highlightedPart = `<span class="${className}" data-chunk-id="${chunkId}">${text}</span>`;
      
      highlightedText = 
        highlightedText.substring(0, start) + 
        highlightedPart + 
        highlightedText.substring(end);
    }
    
    return highlightedText;
  };

  // 新しいハイライトが追加された場合、その位置にスクロール
  useEffect(() => {
    if (highlightedChunkId && contentRef.current) {
      setTimeout(() => {
        // レンダリング後に要素を検索
        const highlightEl = contentRef.current?.querySelector(`[data-chunk-id="${highlightedChunkId}"]`);
        if (highlightEl) {
          highlightEl.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
          });
        }
      }, 100);
    }
  }, [highlightedChunkId]);
  
  // すべてのハイライトをクリア
  const clearAllHighlights = () => {
    setActiveHighlightIds(new Set());
  };

  const filteredMarkdown = getFilteredMarkdown();
  const highlightedMarkdown = getHighlightedMarkdown();

  return (
    <div className="w-1/3 h-full flex flex-col border-l border-secondary-200 bg-white">
      <div className="py-3 px-4 border-b border-secondary-200 flex items-center justify-between">
        <h2 className="text-lg font-medium text-secondary-900">ドキュメント原文</h2>
        <div className="flex items-center space-x-2">
          {activeHighlightIds.size > 0 && (
            <button
              onClick={clearAllHighlights}
              className="text-xs px-2 py-1 bg-secondary-100 hover:bg-secondary-200 rounded transition-colors"
              title="すべてのハイライトをクリア"
            >
              クリア
            </button>
          )}
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
      </div>
      
      <div ref={contentRef} className="flex-1 overflow-y-auto p-4">
        {loading ? (
          <div className="py-6 text-center text-secondary-500">
            <p>読み込み中...</p>
          </div>
        ) : filteredMarkdown ? (
          <pre 
            className="whitespace-pre-wrap text-sm font-normal font-mono"
            dangerouslySetInnerHTML={{ __html: highlightedMarkdown }}
          />
        ) : (
          <div className="py-6 text-center text-secondary-500">
            <p>ドキュメントの内容を読み込めませんでした</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SidePanel;