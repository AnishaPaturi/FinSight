/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        finNavy: {
          900: '#0b132b',
          800: '#1c2541',
          700: '#3a506b',
        },
        finCyan: {
          500: '#00b4d8',
          400: '#48cae4',
          300: '#90e0ef',
        },
        finGreen: {
          500: '#10b981',
          400: '#34d399',
        },
        finRed: {
          500: '#ef4444',
          400: '#f87171',
        }
      }
    },
  },
  plugins: [],
}
