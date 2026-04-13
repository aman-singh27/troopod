import { useState } from 'react';
import { Download, ArrowLeft, Eye, Code } from 'lucide-react';
import ModificationsPanel from '../components/ModificationsPanel';
import AdAnalysisCard from '../components/AdAnalysisCard';
import toast from 'react-hot-toast';

export default function ResultPage({ result, onBack }) {
  const [previewTab, setPreviewTab] = useState('personalized');
  const [showSource, setShowSource] = useState(false);

  const downloadHTML = () => {
    const blob = new Blob([result.modified_html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'personalized-page.html';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('HTML downloaded!');
  };

  return (
    <div className="min-h-screen bg-bg-primary pt-20 pb-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="flex items-center gap-2 text-accent-purple hover:text-accent-bright transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Back
            </button>
            <h1 className="font-syne text-3xl font-bold">AdaptLP Result</h1>
          </div>
          <div className="bg-bg-card border border-border rounded-lg px-4 py-2">
            <p className="text-text-muted text-sm">
              Processed in <span className="text-accent-purple font-600">{(result.processing_time_ms / 1000).toFixed(2)}s</span>
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <AdAnalysisCard analysis={result.ad_analysis} />
          <div className="lg:col-span-2">
            <ModificationsPanel modifications={result.modifications} />
          </div>
        </div>

        <div className="troopod-card p-6">
          <h3 className="font-syne text-lg font-bold mb-4">Preview</h3>
          
          <div className="flex gap-2 mb-4 border-b border-border">
            <button
              onClick={() => setPreviewTab('personalized')}
              className={`px-4 py-2 font-dm-sans transition-colors flex items-center gap-2 ${
                previewTab === 'personalized'
                  ? 'border-b-2 border-accent-purple text-accent-purple'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <Eye className="w-4 h-4" />
              Personalized Page
            </button>
            <button
              onClick={() => setPreviewTab('source')}
              className={`px-4 py-2 font-dm-sans transition-colors flex items-center gap-2 ${
                previewTab === 'source'
                  ? 'border-b-2 border-accent-purple text-accent-purple'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <Code className="w-4 h-4" />
              View Source
            </button>
          </div>

          {previewTab === 'personalized' && (
            <div className="bg-bg-secondary rounded-lg overflow-hidden border border-border">
              <iframe
                srcDoc={result.modified_html}
                title="Personalized Page"
                className="w-full h-screen min-h-96 border-none"
                sandbox="allow-scripts allow-same-origin"
              />
            </div>
          )}

          {previewTab === 'source' && (
            <div className="bg-bg-secondary rounded-lg p-4 overflow-auto max-h-96 border border-border">
              <pre className="text-text-secondary text-xs font-mono whitespace-pre-wrap break-words">
                {result.modified_html}
              </pre>
            </div>
          )}

          <button
            onClick={downloadHTML}
            className="mt-4 btn-primary flex items-center gap-2 w-full justify-center"
          >
            <Download className="w-4 h-4" />
            Download Modified HTML
          </button>
        </div>
      </div>
    </div>
  );
}
