import { useState } from "react";
import axios from "axios";

export default function UploadForm({ setResult }) {
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState("");

const handleFile = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // ✅ Check if the uploaded file is not a PDF
  if (!file.type.includes("pdf")) {
    alert(
      "⚠️ Please upload a PDF file only.\n\nYou can use Google Lens or another tool to extract text from the image and save it as a PDF before uploading."
    );
    return;
  }

  setFileName(file.name);
  const formData = new FormData();
  formData.append("file", file);

  setLoading(true);
  try {
    const res = await axios.post("http://localhost:8000/upload", formData);
    setResult(res.data);
  } catch (error) {
    alert("Upload failed. Please try again.");
    console.error("Upload Error:", error);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="flex flex-col items-center gap-6 p-8 w-full max-w-xl rounded-2xl shadow-2xl bg-gradient-to-br from-sky-100 via-white to-indigo-100">
      <h2 className="text-2xl font-bold text-gray-800">Upload Medical Report</h2>

      <label
        htmlFor="file-upload"
        className="cursor-pointer px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg shadow-md hover:from-blue-600 hover:to-indigo-700 transition duration-200"
      >
        Choose PDF only
      </label>

      <input
        id="file-upload"
        type="file"
        accept=".pdf,image/*"
        onChange={handleFile}
        className="hidden"
      />

      {fileName && (
        <p className="text-sm text-gray-700 font-medium">{fileName}</p>
      )}

      {loading && (
        <p className="text-sm text-gray-600 italic">Processing... please wait</p>
      )}
    </div>
  );
}
