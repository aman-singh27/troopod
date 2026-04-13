export default function AdAnalysisCard({ analysis }) {
  if (!analysis) return null;

  const fields = [
    { label: 'Headline', value: analysis.headline },
    { label: 'Offer', value: analysis.offer },
    { label: 'CTA', value: analysis.cta_text },
    { label: 'Tone', value: analysis.tone },
    { label: 'Audience', value: analysis.target_audience },
    { label: 'Product Type', value: analysis.product_type },
    { label: 'Key Emotion', value: analysis.key_emotion },
  ];

  return (
    <div className="troopod-card p-6">
      <h3 className="font-syne text-lg font-bold mb-4">Ad Analysis</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {fields.map((field) => (
          <div key={field.label}>
            <p className="text-text-muted text-sm mb-1">{field.label}</p>
            <p className="text-text-primary font-600">{field.value}</p>
          </div>
        ))}
      </div>

      {analysis.color_palette && analysis.color_palette.length > 0 && (
        <div className="mt-4">
          <p className="text-text-muted text-sm mb-2">Color Palette</p>
          <div className="flex gap-2">
            {analysis.color_palette.map((color, idx) => (
              <div
                key={idx}
                className="w-12 h-12 rounded-lg border border-border/50"
                style={{ backgroundColor: color }}
                title={color}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
