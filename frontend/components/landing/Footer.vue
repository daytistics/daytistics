<template>
    <footer class="bg-slate-50">
        <div class="mx-auto w-full max-w-screen-xl p-4 py-6 lg:py-8">
            <div class="sm:flex sm:items-center sm:justify-between text-sm text-gray-500">
                <span class="sm:text-center"
                    >Made with &#129505; by the contributors of Daytistics.
                </span>
                <div class="flex flex-row justify-center items-center">
                    <div class="flex flex-row justify-center items-center border-r px-4 gap-3">
                        <NuxtLink
                            v-for="page in legalPages"
                            :to="page.to"
                        >
                            {{ page.title }}
                        </NuxtLink>
                    </div>
                    <div class="flex mt-4 sm:justify-center sm:mt-0 pl-4">
                        <a
                            href="#"
                            class="text-gray-500 hover:text-gray-900"
                        >
                            <svg
                                class="w-4 h-4"
                                aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="currentColor"
                                viewBox="0 0 8 19"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M6.135 3H8V0H6.135a4.147 4.147 0 0 0-4.142 4.142V6H0v3h2v9.938h3V9h2.021l.592-3H5V3.591A.6.6 0 0 1 5.592 3h.543Z"
                                    clip-rule="evenodd"
                                />
                            </svg>
                            <span class="sr-only">Facebook page</span>
                        </a>
                        <a
                            href="#"
                            class="text-gray-500 hover:text-gray-900 ms-5"
                        >
                            <TwitchIcon class="w-4 h-4" />
                            <span class="sr-only">Discord community</span>
                        </a>
                        <a
                            href="#"
                            class="text-gray-500 hover:text-gray-900 ms-5"
                        >
                            <GithubIcon class="w-4 h-4" />
                            <span class="sr-only">GitHub account</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup lang="ts">
import { GithubIcon, LinkedinIcon, YoutubeIcon, HeartIcon, TwitchIcon } from 'lucide-vue-next';

const othersPages = [
    {
        title: 'Documentation',
        to: 'https://docs.daytistics.com',
    },
    {
        title: 'Donate',
        to: 'https://polar.sh/daytistics',
    },
    {
        title: 'Support',
        to: 'https://support.daytistics.com',
    },
];

const actionsPages = [
    {
        title: 'Sign Up',
        to: '/signup',
    },
    {
        title: 'Log In',
        to: '/login',
    },
];

const sectionsPages = [
    {
        title: 'Home',
        to: '/',
    },
    {
        title: 'Features',
        to: '/#features',
    },
    {
        title: 'Pricing',
        to: '/#pricing',
    },
    {
        title: 'Self-Hosting',
        to: '/#self-hosting',
    },
    {
        title: 'FAQ',
        to: '/#faq',
    },
];

const legalPages = [
    {
        title: 'Imprint',
        to: '/legal/imprint',
    },
    {
        title: 'Privacy',
        to: '/legal/privacy',
    },
    {
        title: 'Terms',
        to: '/legal/terms',
    },
    {
        title: 'Cancellation',
        to: '/legal/cancellation',
    },
    {
        title: 'Cookies',
        to: '/legal/cookies',
    },
];
</script>
