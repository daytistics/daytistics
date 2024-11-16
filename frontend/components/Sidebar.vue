<template>
    <aside
        class="flex flex-col items-center w-16 h-screen py-8 overflow-y-auto bg-white border-r rtl:border-l rtl:border-r-0"
    >
        <nav class="flex flex-col flex-1 space-y-6 items-center">
            <NuxtLink to="/app">
                <NuxtImg
                    class="w-12 h-auto"
                    src="/images/logo.png"
                    alt=""
                />
            </NuxtLink>

            <NuxtLink
                to="/chat"
                class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg hover:bg-gray-100"
            >
                <MessageCircleCode class="w-6 h-6" />
            </NuxtLink>
        </nav>

        <div class="flex flex-col space-y-6">
            <NuxtLink
                to="/settings"
                class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg hover:bg-gray-100"
            >
                <Settings class="w-6 h-6" />
            </NuxtLink>
            <button
                type="button"
                class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg hover:bg-gray-100"
            >
                <LogOut class="w-6 h-6" />
            </button>
        </div>
    </aside>
</template>

<script lang="ts" setup>
import {
    BarChartIcon,
    Home,
    LogOut,
    LucideHouse,
    MessageCircleCode,
    MessageSquare,
    Settings,
    ShieldAlert,
    Users,
} from 'lucide-vue-next';

const authStore = useAuthStore();
</script>
