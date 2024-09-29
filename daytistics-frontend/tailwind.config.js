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
