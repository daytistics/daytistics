<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';

const open = ref(false);
const dropdownButtonRef = ref<HTMLButtonElement | null>(null);

const toggleNavbar = () => {
    open.value = !open.value;
};

const navLinkItems = ref([
    { text: 'About Us', href: 'javascript:void(0)' },
    { text: 'Services', href: 'javascript:void(0)' },
    { text: 'Blog', href: 'javascript:void(0)' },
    { text: 'Contact', href: 'javascript:void(0)' },
]);

// Custom composition function to handle click outside
const handleClickOutside = (event: MouseEvent) => {
    if (dropdownButtonRef.value && !dropdownButtonRef.value.contains(event.target as Node)) {
        open.value = false;
    }
};

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
    <!-- ====== Navbar Section Start -->
    <header class="absolute top-0 left-0 z-50 w-full">
        <div class="">
            <LandingNavbar />
        </div>
    </header>
    <!-- ====== Navbar Section End -->

    <!-- ====== Hero Section Start -->
    <div
        class="relative z-10 overflow-hidden bg-white pt-[120px] pb-[110px] md:pt-[150px] lg:pt-[180px]"
    >
        <div class="container mx-auto">
            <div class="flex flex-wrap justify-center -mx-4">
                <div class="w-full px-4">
                    <div class="hero-content mx-auto max-w-[666px] text-center">
                        <span
                            class="block mb-5 text-base font-semibold text-primary sm:text-lg md:text-xl"
                        >
                            <AutoTyping
                                :texts="['Hallo', 'Nein']"
                                class="min-h-7"
                            />
                        </span>
                        <h1
                            class="mb-5 text-3xl font-bold capitalize !leading-[1.208] text-dark sm:text-[42px] xl:text-5xl"
                        >
                            Welcome to Daytistics
                        </h1>
                        <p class="text-base font-medium mb-9 text-body-color md:text-lg">
                            Daytistics is a simple app to track your activities, mood, and journal
                            entries. It helps you discover patterns and improve your well-being.
                            Clean visuals make tracking and insights effortless.
                        </p>
                        <ul class="flex flex-wrap items-center justify-center gap-4">
                            <li>
                                <a
                                    href="javascript:void(0)"
                                    class="inline-flex items-center justify-center py-3 text-base font-medium text-center text-white border border-transparent rounded-md bg-primary px-7 hover:bg-secondary"
                                >
                                    Know More
                                </a>
                            </li>
                            <li>
                                <a
                                    href="javascript:void(0)"
                                    class="inline-flex items-center justify-center py-3 text-base font-medium text-center transition border rounded-md border-primary px-7 text-primary hover:border-primary hover:bg-primary hover:text-white"
                                >
                                    Contact Us
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <span class="absolute top-0 left-0 -z-10">
                <svg
                    width="784"
                    height="619"
                    viewBox="0 0 784 619"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <rect
                        opacity="0.05"
                        x="343.762"
                        y="-429.286"
                        width="681.025"
                        height="859.911"
                        rx="101"
                        transform="rotate(45 343.762 -429.286)"
                        fill="url(#paint0_linear_1414_1006)"
                    />
                    <defs>
                        <linearGradient
                            id="paint0_linear_1414_1006"
                            x1="684.275"
                            y1="-429.286"
                            x2="650.39"
                            y2="509.923"
                            gradientUnits="userSpaceOnUse"
                        >
                            <stop stop-color="#3056D3" />
                            <stop
                                offset="1"
                                stop-color="#3056D3"
                                stop-opacity="0"
                            />
                        </linearGradient>
                    </defs>
                </svg>
            </span>
            <span class="absolute top-0 right-0 -z-10">
                <svg
                    width="577"
                    height="606"
                    viewBox="0 0 577 606"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <rect
                        opacity="0.05"
                        x="880.642"
                        y="206.506"
                        width="619.809"
                        height="680.424"
                        rx="94"
                        transform="rotate(135 880.642 206.506)"
                        fill="url(#paint0_linear_1414_1005)"
                    />
                    <defs>
                        <linearGradient
                            id="paint0_linear_1414_1005"
                            x1="1190.55"
                            y1="206.506"
                            x2="1167.23"
                            y2="949.912"
                            gradientUnits="userSpaceOnUse"
                        >
                            <stop stop-color="#3056D3" />
                            <stop
                                offset="1"
                                stop-color="#3056D3"
                                stop-opacity="0"
                            />
                        </linearGradient>
                    </defs>
                </svg>
            </span>
            <span class="absolute bottom-0 left-1/2 -z-10">
                <svg
                    width="695"
                    height="363"
                    viewBox="0 0 695 363"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <rect
                        opacity="0.05"
                        x="719.109"
                        y="488.892"
                        width="325.482"
                        height="726.494"
                        rx="60"
                        transform="rotate(135 719.109 488.892)"
                        fill="url(#paint0_linear_1414_1009)"
                    />
                    <defs>
                        <linearGradient
                            id="paint0_linear_1414_1009"
                            x1="881.85"
                            y1="488.892"
                            x2="831.383"
                            y2="1280.2"
                            gradientUnits="userSpaceOnUse"
                        >
                            <stop stop-color="#3056D3" />
                            <stop
                                offset="1"
                                stop-color="#3056D3"
                                stop-opacity="0"
                            />
                        </linearGradient>
                    </defs>
                </svg>
            </span>
            <span class="absolute bottom-0 left-1/4 -z-10">
                <svg
                    width="469"
                    height="139"
                    viewBox="0 0 469 139"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <rect
                        opacity="0.05"
                        width="353.669"
                        height="342.737"
                        rx="30"
                        transform="matrix(0.707107 0.707107 0.707107 -0.707107 -12 230.352)"
                        fill="url(#paint0_linear_1414_1011)"
                    />
                    <defs>
                        <linearGradient
                            id="paint0_linear_1414_1011"
                            x1="176.834"
                            y1="3.18915e-07"
                            x2="166.463"
                            y2="374.543"
                            gradientUnits="userSpaceOnUse"
                        >
                            <stop stop-color="#3056D3" />
                            <stop
                                offset="1"
                                stop-color="#3056D3"
                                stop-opacity="0"
                            />
                        </linearGradient>
                    </defs>
                </svg>
            </span>
        </div>
    </div>
    <!-- ====== Hero Section End -->
</template>
