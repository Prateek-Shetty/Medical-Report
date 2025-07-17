import UploadForm from "../components/UploadForm";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Medical Report Analyzer</h1>

      <UploadForm setResult={setResult} />

      {result && (
        <div className="mt-10 w-full max-w-3xl bg-white/90 p-6 rounded-xl shadow-lg prose prose-lg prose-h2:mt-14 prose-h2:mb-4">
          <ReactMarkdown>
            {result.gemini_result
              ?.replace(/Kannada Summary/g, "---\n\n## Kannada Summary")
              ?.replace(/Hindi Summary/g, "---\n\n## Hindi Summary")}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}
