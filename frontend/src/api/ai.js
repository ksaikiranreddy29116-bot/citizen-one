import axios from "axios";

const api = axios.create({
  baseURL: "https://viewing-facelift-glisten.ngrok-free.dev/api/v1",
  headers: {
    "ngrok-skip-browser-warning": "1",
  },
});

export const extractDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    "/welfare/extract-document",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};