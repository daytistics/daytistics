/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./node_modules/flowbite/**/*.{js,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0e9f6e',
        'secondary': '#5850ec',
        'primary-dark': '#16a34a',
        'secondary-dark': '#4f46e5',
      },
      spacing: {
        '75px': '75px',
        '690px': '690px',
        '800px': '800px',
        '8xl': '88rem'
      },
    },
  },
  plugins: [require('flowbite/plugin')]
}


// Für ein Logo mit den Farben #81cc57 (Grün) und #0e4355 (Dunkelblau) könntest du folgende Farbkombinationen für den Dark- und Lightmode nutzen:

// Light Mode:

// Hintergrund: Weiß (#FFFFFF) oder sehr helles Grau (#F5F5F5) für hohe Lesbarkeit
// Text: Dunkelgrau (#333333) oder Schwarz (#000000) für Kontrast
// Akzentfarben: Hellgrau (#D9D9D9) oder Pastellfarben wie Hellgrün (#A9E5AA)
// Dark Mode:

// Hintergrund: Tiefes Dunkelgrau (#1C1C1C) oder Anthrazit (#2E2E2E)
// Text: Hellgrau (#E0E0E0) oder Weiß (#FFFFFF)
// Akzentfarben: Leuchtende Grüntöne (#A3E635) oder Blau (#4FB6C5) für dynamische Effekte
// Diese Kombinationen bieten gute Kontraste und passen harmonisch zu den Hauptfarben des Logos.