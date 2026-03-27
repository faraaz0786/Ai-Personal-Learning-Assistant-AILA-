/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fdf8f6',
          100: '#fbece6',
          200: '#f8d9cd',
          300: '#f2bbab',
          400: '#e8917d',
          500: 'var(--primary)', // Burnt Orange
          600: '#d15e45',
          700: '#af4b38',
          800: '#8f3e30',
          900: '#77352b',
          950: '#401a14',
        },
        secondary: {
          DEFAULT: '#8b6f5a',
          muted: '#6b5e52',
        },
        background: {
          DEFAULT: '#f5f1eb', // warm ivory
          card: '#ffffff',
          alt: '#ede8e1', // deeper warm beige
        },
        'surface-border': '#e7e1d8',
        'surface-text-primary': '#1c1917',
        'surface-text-secondary': '#6b5e52',
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        editorial: ["Georgia", "serif"], // For scholarly accents
        mono: ["JetBrains Mono", "monospace"]
      },
      boxShadow: {
        'soft': '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        'inner-soft': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.03)',
        'academic': '0 4px 6px -1px rgba(28, 25, 23, 0.05), 0 2px 4px -1px rgba(28, 25, 23, 0.03)',
      },
      animation: {
        'blob': 'blob 7s infinite',
      },
      keyframes: {
        blob: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
          '100%': { transform: 'translate(0px, 0px) scale(1)' },
        }
      }
    }
  },
  plugins: [],
}
