import type { Config } from 'tailwindcss';

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
                primary: '#0e9f6e',
                secondary: '#057a55',
                tertiary: '#046c4e',
                'day-gray-light': '#f9fafb',
                'day-gray-medium': '#e5e7eb',
                'day-gray-dark': '#6b7280',
                gradient: {
                    1: '#4ade80',
                    2: '#3b82f6',
                },
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
    plugins: [require('tailgrids/plugin')],
} satisfies Config;
