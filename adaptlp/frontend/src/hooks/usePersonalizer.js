import { useState, useCallback } from 'react';
import { personalizeAPI } from '../utils/api';
import toast from 'react-hot-toast';

export const usePersonalizer = () => {
  const [status, setStatus] = useState('idle');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const personalize = useCallback(async (lpUrl, adInput, adInputType, geminiApiKey) => {
    try {
      setStatus('processing');
      setError(null);
      const data = await personalizeAPI(lpUrl, adInput, adInputType, geminiApiKey);
      setResult(data);
      setStatus('success');
      toast.success('Page personalized successfully!');
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'An error occurred';
      setError(message);
      setStatus('error');
      toast.error(message);
    }
  }, []);

  const reset = useCallback(() => {
    setStatus('idle');
    setResult(null);
    setError(null);
  }, []);

  return { status, result, error, personalize, reset };
};
