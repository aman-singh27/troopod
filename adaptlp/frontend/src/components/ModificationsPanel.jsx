import { Copy, Download } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ModificationsPanel({ modifications }) {
  const downloadHTML = (html) => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'personalized-page.html';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('HTML downloaded!');
  };

  return (
    <div className="troopod-card p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-syne text-lg font-bold">
          {modifications.length} Changes Applied
        </h3>
      </div>

      <div className="space-y-4 max-h-96 overflow-y-auto">
        {modifications.map((mod, idx) => (
          <div key={idx} className="bg-bg-secondary rounded-lg p-4 border border-border/50">
            <div className="flex items-start gap-3 mb-2">
              <span className="bg-accent-purple/20 text-accent-purple px-2 py-1 rounded text-xs font-dm-sans font-600">
                {mod.element_type.toUpperCase()}
              </span>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex gap-2 items-start">
                <p className="text-text-muted line-through flex-1">{mod.original_text}</p>
              </div>
              <div className="flex gap-2 items-start">
                <span className="text-accent-teal mt-0.5">→</span>
                <p className="text-text-primary font-600 flex-1">{mod.replacement_text}</p>
              </div>
            </div>
            
            <p className="text-text-muted text-xs italic mt-3">
              💡 {mod.cro_reason}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
