import { Mail } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full bg-bg-primary/80 backdrop-blur border-b border-border z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-purple rounded-full flex items-center justify-center">
            <span className="text-accent-light font-syne font-bold">∞</span>
          </div>
          <span className="font-syne font-bold text-xl gradient-text">troopod</span>
        </div>
        <a href="/" className="text-text-secondary hover:text-text-primary transition-colors">
          Home
        </a>
      </div>
    </nav>
  );
}
