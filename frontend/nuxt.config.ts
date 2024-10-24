import { meta } from 'eslint-plugin-prettier';
import { name } from 'eslint-plugin-prettier/recommended';
import type { build } from 'nuxt';
import type { devtools } from 'vue';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    // NUXT CONFIGURATION
    compatibilityDate: '2024-04-03',
    ssr: false,
    devtools: {
        enabled: true,

        timeline: {
            enabled: true,
        },
    },

    build: {
        transpile: ['@vuepic/vue-datepicker'],
    },

    components: [
        { path: '~/components/daytistic', prefix: 'Daytistic' },
        { path: '~/components/dashboard', prefix: 'Dashboard' },
        '~/components',
    ],

    runtimeConfig: {
        public: {
            imprintAddress: process.env.IMPRINT_ADDRESS,
            imprintPublisher: process.env.IMPRINT_PUBLISHER,
            imprintEmail: process.env.IMPRINT_EMAIL,
        },
    },

    css: ['~/assets/css/fonts.css', '~/assets/css/tailwind.css'],

    // NITRO CONFIGURATION
    nitro: {
        devProxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/api',
                changeOrigin: true,
            },
        },
    },

    // MODULES & MODULE CONFIGURATION
    modules: [
        '@nuxt/image',
        '@nuxtjs/tailwindcss',
        '@nuxt/test-utils/module',
        '@pinia/nuxt',
        'nuxt-aos',
    ],

    image: {
        dir: 'assets/media',
    },
});
