import { useState, useEffect } from "react";
import AdInput from "../components/AdInput";
import LPInput from "../components/LPInput";
import ProcessingStatus from "../components/ProcessingStatus";
import { usePersonalizer } from "../hooks/usePersonalizer";

export default function HomePage({ onResultReady }) {
  const [lpUrl, setLpUrl] = useState("");
  const [adInput, setAdInput] = useState(null);
  const [adInputType, setAdInputType] = useState(null);
  const [geminiApiKey, setGeminiApiKey] = useState("");
  const [processingStep, setProcessingStep] = useState(0);
  const { status, result, error, personalize, reset } = usePersonalizer();

  useEffect(() => {
    if (result) {
      onResultReady(result);
    }
  }, [result, onResultReady]);

  useEffect(() => {
    if (status === "processing") {
      const interval = setInterval(() => {
        setProcessingStep((p) => (p < 4 ? p + 1 : 4));
      }, 2500);
      return () => clearInterval(interval);
    } else {
      setProcessingStep(0);
    }
  }, [status]);

  const handleAdInputChange = (input, type) => {
    setAdInput(input);
    setAdInputType(type);
  };

  const handleSubmit = () => {
    if (!lpUrl || !adInput) {
      alert("Please provide both a landing page URL and an ad input");
      return;
    }
    setProcessingStep(0);
    personalize(lpUrl, adInput, adInputType, geminiApiKey.trim() || null);
  };

  return (
    <div className="min-h-screen bg-bg-primary pt-20 pb-12">
      {status === "processing" && (
        <ProcessingStatus currentStep={processingStep} />
      )}

      <div className="max-w-6xl mx-auto px-4">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-block bg-accent-purple/10 border border-accent-purple/20 rounded-pill px-4 py-2 mb-4">
            <p className="text-accent-purple text-sm font-dm-sans font-600">
              AI-Powered CRO & Personalization
            </p>
          </div>

          <h1 className="font-syne text-5xl font-bold mb-4">
            Personalize Your <span className="gradient-text">Landing Page</span>{" "}
            with AI
          </h1>

          <p className="text-text-secondary text-lg max-w-2xl mx-auto">
            Transform any landing page to match your ad creative — powered by
            AI-driven CRO and message personalization.
          </p>
        </div>

        {/* Input Form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <AdInput
            onInputChange={handleAdInputChange}
            isLoading={status === "processing"}
          />
          <LPInput
            value={lpUrl}
            onChange={setLpUrl}
            isLoading={status === "processing"}
          />
        </div>

        <div className="troopod-card p-6 mb-8">
          <h3 className="font-syne text-lg font-bold mb-2">
            Optional: Use Your Own Gemini API Key
          </h3>
          <p className="text-text-muted text-sm mb-3">
            Leave blank to use server key. This key is used one-time for this
            request and is not stored.
          </p>
          <input
            type="password"
            value={geminiApiKey}
            onChange={(e) => setGeminiApiKey(e.target.value)}
            disabled={status === "processing"}
            placeholder="AIza..."
            className="w-full bg-bg-secondary border border-border rounded-lg px-4 py-3 text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-purple transition-colors"
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={status === "processing" || !lpUrl || !adInput}
          className="w-full btn-primary py-4 text-lg font-dm-sans font-600 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
        >
          Generate Personalized Page →
        </button>

        {error && (
          <div className="mt-6 bg-red-500/10 border border-red-500/20 rounded-lg p-4">
            <p className="text-red-400 font-dm-sans">{error}</p>
          </div>
        )}

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <div className="troopod-card p-6 text-center">
            <p className="font-syne text-3xl font-bold gradient-text">25%</p>
            <p className="text-text-muted mt-2">Average Conversion Lift</p>
          </div>
          <div className="troopod-card p-6 text-center">
            <p className="font-syne text-3xl font-bold gradient-text">2x</p>
            <p className="text-text-muted mt-2">Faster Optimization</p>
          </div>
          <div className="troopod-card p-6 text-center">
            <p className="font-syne text-3xl font-bold gradient-text">5x</p>
            <p className="text-text-muted mt-2">More Affordable</p>
          </div>
        </div>
      </div>
    </div>
  );
}
