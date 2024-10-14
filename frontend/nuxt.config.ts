import type { build } from 'nuxt';
import type { devtools } from 'vue';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
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

    modules: [
        '@nuxt/image',
        '@nuxtjs/tailwindcss',
        '@nuxt/test-utils/module',
        '@pinia/nuxt',
        'nuxt-aos',
    ],

    nitro: {
        devProxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/api',
                changeOrigin: true,
            },
        },
    },

    image: {
        dir: 'assets/graphics',
    },
});
