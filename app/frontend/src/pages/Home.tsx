import { useEffect, useState } from "react";
import { uploadPdf, getDocuments } from "../api/docs";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    const docs = await getDocuments();
    setDocuments(docs);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      const res = await uploadPdf(file);
      await fetchDocuments();
      navigate(`/chat/${res.document_id}`);
    } catch (err) {
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">📄 PDF アップロード</h1>

      <div className="flex items-center space-x-4">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="file-input file-input-bordered"
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? "アップロード中..." : "アップロード"}
        </button>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">📚 アップロード済みPDF</h2>
        <ul className="list-disc pl-5 space-y-1">
          {documents.map((doc) => (
            <li key={doc.document_id}>
              <button
                onClick={() => navigate(`/chat/${doc.document_id}`)}
                className="text-blue-600 hover:underline"
              >
                {doc.title}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
