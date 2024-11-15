/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.core.{js,ts}',
    ],
    theme: {
        extend: {
            colors: {
                'day-primary': '#0e9f6e',
                'day-secondary': '#057a55',
                'day-tertiary': '#046c4e',
                'day-gradient-from': '#4ade80',
                'day-gradient-to': '#3b82f6',
            },
            spacing: {
                '75px': '75px',
                '690px': '690px',
                '800px': '800px',
                '8xl': '88rem',
            },
        },
        fontFamily: {
            sans: [
                '"Inter", sans-serif',
                {
                    fontFeatureSettings: '"cv11", "ss01"',
                    fontVariationSettings: '"opsz" 32',
                },
            ],
        },
    },
    plugins: [],
};
