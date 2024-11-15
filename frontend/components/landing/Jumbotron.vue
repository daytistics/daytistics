<template>
    <div
        class="bg-gradient-to-r from-day-gradient-from to-day-gradient-to font-sans px-6 pb-12 pt-40"
    >
        <div class="container mx-auto flex flex-col justify-center items-center text-center">
            <h2 class="text-white sm:text-4xl text-3xl font-bold mb-4">Welcome to Daytistics</h2>
            <p class="text-white text-center mb-8 min-h-7 text-lg">
                <AutoTyping />
            </p>

            <NuxtLink
                v-if="isAuthenticated"
                to="/app"
                class="bg-gray-200/30 p-4 rounded-xl text-xl font-semibold text-white flex flex-row items-center gap-2"
            >
                <Compass />
                <span>Dashboard</span>
            </NuxtLink>
            <NuxtLink
                v-else
                to="/login"
                class="bg-gray-200/30 p-4 rounded-xl text-xl font-semibold text-white flex flex-row items-center gap-2"
            >
                <LogIn />
                <span>Get Started</span>
            </NuxtLink>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { LogIn, Compass } from 'lucide-vue-next';

const isAuthenticated = await useAuthStore().isAuthenticated();
</script>
