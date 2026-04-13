import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const personalizeAPI = async (lpUrl, adInput, adInputType, geminiApiKey) => {
  const formData = new FormData();
  formData.append('lp_url', lpUrl);
  
  if (adInputType === 'file') {
    formData.append('ad_image', adInput);
  } else if (adInputType === 'url') {
    formData.append('ad_url', adInput);
  }

  if (geminiApiKey) {
    formData.append('gemini_api_key', geminiApiKey);
  }
  
  const response = await apiClient.post('/api/personalize', formData);
  return response.data;
};
