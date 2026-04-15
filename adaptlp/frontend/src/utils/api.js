import axios from "axios";

const hostname =
  typeof window !== "undefined" ? window.location.hostname : "localhost";
const defaultApiHost = hostname === "127.0.0.1" ? "127.0.0.1" : "localhost";
const API_BASE_URL =
  import.meta.env.VITE_API_URL || `http://${defaultApiHost}:8000`;

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export const personalizeAPI = async (
  lpUrl,
  adInput,
  adInputType,
  geminiApiKey,
) => {
  const formData = new FormData();
  formData.append("lp_url", lpUrl);

  if (adInputType === "file") {
    formData.append("ad_image", adInput);
  } else if (adInputType === "url") {
    formData.append("ad_url", adInput);
  }

  if (geminiApiKey) {
    formData.append("gemini_api_key", geminiApiKey);
  }

  try {
    const response = await apiClient.post("/api/personalize", formData);
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      throw new Error(
        "Request timed out after 60 seconds. Try a smaller image, another landing page URL, or your own Gemini API key.",
      );
    }
    throw error;
  }
};
