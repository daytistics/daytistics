<template>
    <div class="fixed top-0 left-0 right-0 z-50">
        <div class="bg-white/60 bg-opacity-80 backdrop-blur-sm text-gray-900 shadow-md">
            <div class="mx-auto px-4 py-5">
                <div class="flex items-center justify-between">
                    <NuxtLink
                        to="/"
                        class="flex items-center text-2xl font-black uppercase text-transparent bg-gradient-to-tr bg-clip-text from-day-primary to-day-secondary transition hover:scale-105"
                    >
                        Daytistics
                    </NuxtLink>

                    <div class="hidden md:flex space-x-4 items-center justify-center">
                        <div
                            v-for="item in homeSections"
                            :key="item.title"
                            class="flex flex-row items-center justify-center"
                        >
                            <NuxtLink
                                :to="item.link"
                                class="hover:text-day-primary transition"
                            >
                                {{ item.title }}
                            </NuxtLink>
                        </div>

                        <Menu
                            as="div"
                            class="relative"
                        >
                            <MenuButton class="flex items-center space-x-2 focus:outline-none">
                                <NuxtImg
                                    src="/images/logo.png"
                                    alt="Logo"
                                    class="w-8 h-8 rounded-full"
                                />
                                <ChevronDownIcon class="w-4 h-4" />
                            </MenuButton>

                            <transition
                                enter-active-class="transition duration-100 ease-out"
                                enter-from-class="transform scale-95 opacity-0"
                                enter-to-class="transform scale-100 opacity-100"
                                leave-active-class="transition duration-75 ease-in"
                                leave-from-class="transform scale-100 opacity-100"
                                leave-to-class="transform scale-95 opacity-0"
                            >
                                <MenuItems
                                    class="absolute right-0 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-[60]"
                                >
                                    <div class="px-1 py-1">
                                        <MenuItem
                                            v-slot="{ active }"
                                            v-for="action in userActions.filter(
                                                (action) => action.authRequired == isAuthenticated
                                            )"
                                        >
                                            <NuxtLink
                                                v-if="action.link"
                                                :to="action.link"
                                                :class="[
                                                    active
                                                        ? 'bg-day-primary text-white'
                                                        : 'text-gray-900',
                                                    'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                                                ]"
                                            >
                                                <component
                                                    :is="action.icon"
                                                    class="w-5 mr-2"
                                                />
                                                <span>{{ action.title }}</span>
                                            </NuxtLink>
                                            <button
                                                v-else-if="action.function"
                                                @click="action.function"
                                                :class="[
                                                    active
                                                        ? 'bg-day-primary text-white'
                                                        : 'text-gray-900',
                                                    'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                                                ]"
                                            >
                                                <component
                                                    :is="action.icon"
                                                    class="w-5 mr-2"
                                                />
                                                <span>{{ action.title }}</span>
                                            </button>
                                        </MenuItem>
                                    </div>
                                    <div
                                        class="px-1 py-1"
                                        v-if="isAuthenticated"
                                    >
                                        <MenuItem v-slot="{ active }">
                                            <span
                                                :class="[
                                                    active
                                                        ? 'bg-day-primary text-white'
                                                        : 'text-gray-900',
                                                    'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                                                ]"
                                            >
                                                <HandCoinsIcon class="w-5 mr-2" />
                                                10k Tokens
                                            </span>
                                        </MenuItem>
                                    </div>
                                </MenuItems>
                            </transition>
                        </Menu>
                    </div>

                    <button
                        @click="isMenuOpen = !isMenuOpen"
                        class="md:hidden focus:outline-none z-50"
                    >
                        <MenuIcon
                            v-if="!isMenuOpen"
                            class="w-6 h-6"
                        />
                        <XIcon
                            v-else
                            class="w-6 h-6"
                        />
                    </button>
                </div>
            </div>
        </div>

        <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="transform -translate-y-full opacity-0"
            enter-to-class="transform translate-y-0 opacity-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="transform translate-y-0 opacity-100"
            leave-to-class="transform -translate-y-full opacity-0"
        >
            <div
                v-if="isMenuOpen"
                class="md:hidden bg-purple-50 bg-opacity-80 backdrop-blur-sm shadow-md fixed top-[72px] left-0 right-0 z-40"
            >
                <div class="px-2 pt-2 pb-3 space-y-1">
                    <NuxtLink
                        v-for="item in homeSections"
                        :key="item.title"
                        :to="item.link"
                        class="block px-3 py-2 rounded-md text-base font-medium hover:text-day-primary transition"
                        @click="isMenuOpen = false"
                    >
                        {{ item.title }}
                    </NuxtLink>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue';
import { ChevronDownIcon, MenuIcon, XIcon, Home } from 'lucide-vue-next';
import { HandCoinsIcon, LogInIcon, NotebookPen, Settings, LogOut } from 'lucide-vue-next';
import { useAuthStore } from '~/stores/auth-store';

const isMenuOpen = ref(false);
const isAuthenticated = ref(false);

const homeSections = [
    { title: "We're hiring 💻", link: '/#features' },
    { title: 'Feedback ⭐', link: '/#features' },
];

const userActions = [
    { title: 'Log In', link: '/login', icon: LogInIcon, authRequired: false },
    { title: 'Sign Up', link: '/signup', icon: NotebookPen, authRequired: false },
    { title: 'Dashboard', link: '/app', icon: Home, authRequired: true },
    { title: 'Settings', link: '/settings', icon: Settings, authRequired: true },
    {
        title: 'Log Out',
        function: async () => await useAuthStore().logout(),
        icon: LogOut,
        authRequired: true,
    },
];

onMounted(async () => {
    if (import.meta.client) {
        isAuthenticated.value = await useAuthStore().isAuthenticated();
    }
});
</script>
