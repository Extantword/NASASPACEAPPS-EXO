/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'space-dark': '#0f0f23',
        'space-blue': '#1a1a2e',
        'space-purple': '#16213e',
        'cosmic-pink': '#f093fb',
        'cosmic-red': '#f5576c',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}