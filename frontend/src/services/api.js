import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function uploadPdf(formData) {
  const response = await api.post("/upload", formData);

  return response.data;
}