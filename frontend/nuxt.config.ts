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
            backendUrl: process.env.BACKEND_URL,
            imprintAddress: process.env.IMPRINT_ADDRESS,
            imprintPublisher: process.env.IMPRINT_PUBLISHER,
            imprintEmail: process.env.IMPRINT_EMAIL,
        },
    },

    // NITRO CONFIGURATION
    nitro: {
        devProxy: {
            '/api': {
                target: `${process.env.BACKEND_URL}/api`,
                changeOrigin: true,
                prependPath: true,
            },
        },
    },

    app: {
        head: {
            link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.png' }],
        },
    },

    css: ['~/assets/css/fonts.css', '~/assets/css/tailwind.css'],

    // MODULES & MODULE CONFIGURATION
    modules: [
        '@nuxt/image',
        '@nuxtjs/tailwindcss',
        '@nuxt/test-utils/module',
        '@pinia/nuxt',
        'nuxt-aos',
        // '@sidebase/nuxt-auth',
    ],

    image: {
        dir: 'assets/media',
    },
});
