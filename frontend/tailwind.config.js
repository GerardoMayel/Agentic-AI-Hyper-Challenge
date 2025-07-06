/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        zurich: {
          blue: '#0066CC',
          'dark-blue': '#004499',
          'light-blue': '#E6F3FF',
          gray: '#666666',
          'light-gray': '#F5F5F5'
        }
      },
    },
  },
  plugins: [],
} 