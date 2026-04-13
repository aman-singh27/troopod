/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{js,jsx}', './index.html'],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#08080f',
        'bg-secondary': '#0f0f1a',
        'bg-card': '#13131f',
        'bg-card-hover': '#1a1a2e',
        'border': 'rgba(124, 58, 237, 0.2)',
        'border-hover': 'rgba(124, 58, 237, 0.5)',
        'accent-purple': '#7c3aed',
        'accent-purple-bright': '#8b5cf6',
        'accent-purple-light': '#a78bfa',
        'accent': '#7c3aed',
        'accent-bright': '#8b5cf6',
        'accent-light': '#a78bfa',
        'accent-teal': '#2dd4bf',
        'text-primary': '#ffffff',
        'text-secondary': '#94a3b8',
        'text-muted': '#475569',
      },
      fontFamily: {
        'syne': ['Syne', 'sans-serif'],
        'dm-sans': ['DM Sans', 'sans-serif'],
      },
      borderRadius: {
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'pill': '9999px',
      },
      boxShadow: {
        'purple': '0 0 40px rgba(124, 58, 237, 0.15)',
      },
      backgroundImage: {
        'gradient-hero': 'linear-gradient(135deg, #2dd4bf, #7c3aed, #a78bfa)',
        'gradient-purple': 'linear-gradient(135deg, #7c3aed, #a78bfa)',
      },
      animation: {
        'pulse-purple': 'pulse-purple 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'pulse-purple': {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 40px rgba(124, 58, 237, 0.15)' },
          '50%': { opacity: '0.8', boxShadow: '0 0 20px rgba(124, 58, 237, 0.1)' },
        }
      }
    },
  },
  plugins: [],
};
