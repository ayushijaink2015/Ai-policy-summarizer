import { useState } from "react";
import { uploadPdf } from "../services/api";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
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
    setSummary("");
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("Uploading file...");

      const result = await uploadPdf(formData);

      console.log("Response received:", result);

      setSummary(result.summary || "No summary returned.");
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

      <br />
      <br />

      {error && <div style={{ color: "red" }}>{error}</div>}

      <h3>Summary</h3>

      <p>{summary}</p>
    </>
  );
}

export default UploadForm;