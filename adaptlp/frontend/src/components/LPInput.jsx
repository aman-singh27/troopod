export default function LPInput({ value, onChange, isLoading }) {
  return (
    <div className="troopod-card p-6">
      <h3 className="font-syne text-lg font-bold mb-4">Landing Page URL</h3>
      <input
        type="url"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={isLoading}
        placeholder="https://yourstore.com/product"
        className="w-full bg-bg-secondary border border-border rounded-lg px-4 py-3 text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-purple transition-colors"
      />
      <p className="text-text-muted text-sm mt-2">We'll fetch and analyze your existing page</p>
    </div>
  );
}
