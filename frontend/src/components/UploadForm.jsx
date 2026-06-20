import { useState } from "react";
import { uploadPdf } from "../services/api";
import SummaryCard from "./SummaryCard";
import LoadingSpinner from "./LoadingSpinner";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  

  function handleFileChange(event) {
    setFile(event.target.files[0] ?? null);
    setError("");
  }

  async function handleUpload() {
    if (!file) {
      alert("Please select a PDF");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("Uploading file...");

      const result = await uploadPdf(formData);
      setSummaryData(result);

      console.log("Response received:", result);
    } catch (error) {
      console.error("Upload error:", error);

      if (error.response) {
        console.log("Status:", error.response.status);
        console.log("Response data:", error.response.data);
        setError(`Upload failed: ${error.response.status}`);
      } else if (error.request) {
        console.log("No response received from server.");
        setError("Upload failed: no response received from server.");
      } else {
        setError(`Upload failed: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <h2>Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
      />

      <br />
      <br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      {loading && <LoadingSpinner />}

      {summaryData && (
        <div className="mt-6">
          <SummaryCard
            filename={summaryData.filename}
            status={summaryData.status}
            createdAt={summaryData.created_at}
            summary={summaryData.summary}
          />
        </div>
      )}

      <br />
      <br />

      {error && <div style={{ color: "red" }}>{error}</div>}
    </>
  );
}

export default UploadForm;