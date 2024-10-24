/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.core.{js,ts}',
        './node_modules/flowbite/**/*.{js,ts}',
    ],
    theme: {
        extend: {
            colors: {
                primary: '#0e9f6e',
                secondary: '#057a55',
                accent: '#3f83f8',
                'primary-dark': '#16a34a',
                'secondary-dark': '#046c4e',
                'accent-dark': '#3f83f8',
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
    plugins: [require('flowbite/plugin')],
};
