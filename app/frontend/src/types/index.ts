export interface Chunk {
    chunk_id: string;
    text: string;
    chapter: string;
    position: number;
  }
  
  export interface Citation {
    chunk_id: string;
    text: string;
    chapter: string;
  }
  
  export interface ChatResponse {
    answer: string;
    citations: Citation[];
  }
  
  export interface DocumentInfo {
    document_id: string;
    title: string;
  }
  