import { CheckCircle, Loader, AlertCircle } from 'lucide-react';

export default function ProcessingStatus({ currentStep }) {
  const steps = [
    { id: 1, name: 'Analyzing Ad Creative', desc: 'Extracting messaging and visual elements' },
    { id: 2, name: 'Fetching Landing Page', desc: 'Loading and parsing your page' },
    { id: 3, name: 'Generating CRO Strategy', desc: 'Planning optimizations' },
    { id: 4, name: 'Applying Personalizations', desc: 'Modifying page content' },
  ];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="troopod-card p-8 max-w-md w-full mx-4">
        <h2 className="font-syne text-2xl font-bold mb-8 gradient-text">Processing Your Page</h2>
        
        <div className="space-y-6">
          {steps.map((step, idx) => {
            const isActive = idx < currentStep;
            const isCurrent = idx === currentStep;
            const isCompleted = idx < currentStep;

            return (
              <div key={step.id} className="flex gap-4">
                <div className="flex flex-col items-center">
                  {isCompleted ? (
                    <CheckCircle className="w-6 h-6 text-accent-teal" />
                  ) : isCurrent ? (
                    <div className="animate-pulse-purple w-6 h-6 rounded-full border-2 border-accent-purple" />
                  ) : (
                    <div className="w-6 h-6 rounded-full border-2 border-text-muted" />
                  )}
                  {idx < steps.length - 1 && (
                    <div className={`w-0.5 h-8 mt-2 ${isActive ? 'bg-accent-purple' : 'bg-text-muted'}`} />
                  )}
                </div>
                
                <div className="flex-1 pt-0.5">
                  <p className={`font-dm-sans font-600 ${isCurrent ? 'text-accent-purple' : isCompleted ? 'text-text-secondary' : 'text-text-muted'}`}>
                    {step.name}
                  </p>
                  <p className="text-text-muted text-sm">{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        <p className="text-text-muted text-center text-sm mt-8">
          Estimated time: 8-10 seconds
        </p>
      </div>
    </div>
  );
}
