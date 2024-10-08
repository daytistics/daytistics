import type { devtools } from 'vue';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    ssr: false,
    compatibilityDate: '2024-04-03',
    devtools: {
        enabled: true,

        timeline: {
            enabled: true,
        },
    },
    components: [
        { path: '~/components/daytistic', prefix: 'Daytistic' },
        { path: '~/components/dashboard', prefix: 'Dashboard' },
        '~/components',
    ],

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
