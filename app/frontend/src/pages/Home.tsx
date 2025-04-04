import { useEffect, useState } from "react";
import { uploadPdf, getDocuments, deleteDocument } from "../api/docs";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<string>("準備中...");
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch (error) {
      console.error("ドキュメント取得エラー:", error);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    
    // アップロード処理中の状態表示を更新するタイマー
    const progressMessages = [
      "PDFをアップロード中...",
      "PDFをMarkdownに変換中...(時間がかかる場合があります)",
      "Markdownをヘッダーベースでチャンク分割中...",
      "ベクトル化処理中...",
      "インデックスを作成中...",
      "もうしばらくお待ちください..."
    ];
    
    let messageIndex = 0;
    setUploadProgress(progressMessages[messageIndex]);
    
    const progressTimer = setInterval(() => {
      messageIndex = (messageIndex + 1) % progressMessages.length;
      setUploadProgress(progressMessages[messageIndex]);
    }, 4000);
    
    try {
      const res = await uploadPdf(file);
      clearInterval(progressTimer);
      await fetchDocuments();
      navigate(`/chat/${res.document_id}`);
    } catch (err) {
      clearInterval(progressTimer);
      alert("アップロードに失敗しました");
    } finally {
      setUploading(false);
      setUploadProgress("準備中...");
    }
  };

  const handleDelete = async (documentId: string, event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    if (!confirm("このドキュメントを削除してもよろしいですか？")) return;
    try {
      await deleteDocument(documentId);
      await fetchDocuments();
    } catch (err) {
      alert("削除に失敗しました");
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        setFile(droppedFile);
      } else {
        alert("PDFファイルのみアップロード可能です");
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-primary-800 mb-4">PDFチャット</h1>
          <p className="text-xl text-secondary-600">PDFをアップロードして、内容について対話しましょう。</p>
        </div>
        
        <div 
          className={`border-2 border-dashed rounded-xl p-10 mb-8 text-center transition-all duration-200 ${
            isDragging 
              ? "border-primary-500 bg-primary-50" 
              : "border-secondary-300 hover:border-primary-400 hover:bg-secondary-50"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center space-y-4">
            <svg 
              className={`w-16 h-16 ${isDragging ? "text-primary-500" : "text-secondary-400"}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={1.5} 
                d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
              />
            </svg>
            
            <div>
              <p className="text-lg mb-2">
                {file ? file.name : "PDFファイルをドラッグ＆ドロップ"}
              </p>
              <p className="text-secondary-500 text-sm mb-4">または</p>
              <label 
                htmlFor="file-upload"
                className="cursor-pointer bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 inline-block"
              >
                ファイルを選択
                <input
                  id="file-upload"
                  type="file"
                  accept="application/pdf"
                  onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                  className="hidden"
                />
              </label>
            </div>
            
            {file && (
              <div className="mt-4 w-full">
                <button
                  onClick={handleUpload}
                  disabled={uploading}
                  className={`py-2 px-6 rounded-md font-medium text-white w-full ${
                    uploading
                      ? "bg-secondary-400 cursor-not-allowed"
                      : "bg-accent-600 hover:bg-accent-700 transition-colors duration-200"
                  }`}
                >
                  {uploading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      アップロード中
                    </span>
                  ) : (
                    "アップロード"
                  )}
                </button>
                
                {uploading && (
                  <div className="mt-3 text-sm text-secondary-600">
                    <p className="animate-pulse">{uploadProgress}</p>
                    <p className="mt-1 text-xs">PDFの変換処理には時間がかかります。<br />ページ数が多いほど処理時間が長くなります。</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-card">
          <div className="px-6 py-4 border-b border-secondary-200">
            <h2 className="text-lg font-medium text-secondary-900">アップロード済みPDF</h2>
          </div>
          
          <div className="divide-y divide-secondary-200">
            {documents.length === 0 ? (
              <div className="py-8 text-center text-secondary-500">
                <p>アップロードされたPDFはありません</p>
              </div>
            ) : (
              documents.map((doc) => (
                <div 
                  key={doc.document_id} 
                  className="flex items-center justify-between px-6 py-4 hover:bg-secondary-50 transition-colors duration-150 cursor-pointer"
                  onClick={() => navigate(`/chat/${doc.document_id}`)}
                >
                  <div className="flex items-center space-x-3">
                    <svg className="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                    </svg>
                    <span className="font-medium text-secondary-900">
                      {doc.title}
                    </span>
                  </div>

                  <div className="flex items-center">
                    <button
                      onClick={(e) => handleDelete(doc.document_id, e)}
                      className="text-secondary-400 hover:text-red-500 transition-colors duration-150"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
