<template>
    <div class="flex h-screen bg-gray-900 text-white">
        <!-- Desktop Sidebar -->
        <div
            :class="[
                'hidden md:flex md:flex-col transition-all duration-300 ease-in-out',
                isCollapsed ? 'md:w-16' : 'md:w-64',
            ]"
        >
            <!-- Sidebar Header -->
            <div class="flex items-center justify-between p-4 border-b border-gray-700">
                <div
                    class="flex items-center space-x-2"
                    v-if="!isCollapsed"
                >
                    <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                        <span class="text-black font-bold text-xl">v</span>
                    </div>
                    <span class="font-semibold text-lg">Vercel</span>
                </div>
                <button
                    @click="toggleSidebar"
                    class="p-1 rounded-md hover:bg-gray-700"
                >
                    <ChevronLeft v-if="!isCollapsed" />
                    <ChevronRight v-else />
                </button>
            </div>

            <!-- Navigation Items -->
            <nav class="flex-1 overflow-y-auto">
                <ul class="p-2 space-y-2">
                    <li
                        v-for="item in navItems"
                        :key="item.name"
                    >
                        <a
                            href="#"
                            :class="[
                                'flex items-center p-2 rounded-md transition-colors duration-200',
                                isCollapsed ? 'justify-center' : 'space-x-3',
                                item.active ? 'bg-gray-700' : 'hover:bg-gray-800',
                            ]"
                        >
                            <component
                                :is="item.icon"
                                class="h-5 w-5"
                            />
                            <span v-if="!isCollapsed">{{ item.name }}</span>
                        </a>
                    </li>
                </ul>
            </nav>

            <!-- Bottom Section -->
            <div class="p-4 border-t border-gray-700">
                <a
                    href="#"
                    :class="[
                        'flex items-center rounded-md transition-colors duration-200 hover:bg-gray-800',
                        isCollapsed ? 'justify-center p-2' : 'space-x-3 p-2',
                    ]"
                >
                    <DollarSign class="h-5 w-5" />
                    <span v-if="!isCollapsed">10k Tokens</span>
                </a>
            </div>
        </div>

        <!-- Mobile Sidebar (Slide-out) -->
        <div
            :class="[
                'fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 transform transition-transform duration-300 ease-in-out md:hidden',
                isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full',
            ]"
        >
            <div class="flex flex-col h-full">
                <div class="flex items-center justify-between p-4 border-b border-gray-700">
                    <div class="flex items-center space-x-2">
                        <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                            <span class="text-black font-bold text-xl">v</span>
                        </div>
                        <span class="font-semibold text-lg">Vercel</span>
                    </div>
                    <button
                        @click="toggleMobileSidebar"
                        class="p-1 rounded-md hover:bg-gray-700"
                    >
                        <X class="h-6 w-6" />
                    </button>
                </div>

                <div class="p-4">
                    <div class="relative">
                        <input
                            type="text"
                            placeholder="Search"
                            class="w-full bg-gray-800 rounded-md py-2 pl-8 pr-4 focus:outline-none focus:ring-2 focus:ring-gray-600"
                        />
                        <Search class="absolute left-2 top-2.5 h-5 w-5 text-gray-400" />
                    </div>
                </div>

                <nav class="flex-1 overflow-y-auto">
                    <ul class="p-2 space-y-2">
                        <li
                            v-for="item in navItems"
                            :key="item.name"
                        >
                            <a
                                href="#"
                                :class="[
                                    'flex items-center space-x-3 p-2 rounded-md transition-colors duration-200',
                                    item.active ? 'bg-gray-700' : 'hover:bg-gray-800',
                                ]"
                            >
                                <component
                                    :is="item.icon"
                                    class="h-5 w-5"
                                />
                                <span>{{ item.name }}</span>
                            </a>
                        </li>
                    </ul>
                </nav>

                <div class="p-4 border-t border-gray-700">
                    <a
                        href="#"
                        class="flex items-center space-x-3 p-2 rounded-md transition-colors duration-200 hover:bg-gray-800"
                    >
                        <User class="h-5 w-5" />
                        <span>10k Tokens</span>
                    </a>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col">
            <!-- Mobile Top Bar -->
            <div class="md:hidden flex items-center justify-between p-4 bg-gray-800">
                <button
                    @click="toggleMobileSidebar"
                    class="p-1 rounded-md hover:bg-gray-700"
                >
                    <Menu class="h-6 w-6" />
                </button>
                <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                    <span class="text-black font-bold text-xl">v</span>
                </div>
            </div>

            <!-- Mobile Bottom Navigation -->
            <div
                class="md:hidden fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700"
            >
                <nav class="flex justify-around">
                    <a
                        v-for="item in navItems"
                        :key="item.name"
                        href="#"
                        :class="[
                            'flex flex-col items-center p-2 transition-colors duration-200',
                            item.active ? 'text-white' : 'text-gray-400 hover:text-white',
                        ]"
                    >
                        <component
                            :is="item.icon"
                            class="h-6 w-6"
                        />
                        <span class="text-xs mt-1">{{ item.name }}</span>
                    </a>
                </nav>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import {
    ChevronLeft,
    ChevronRight,
    Search,
    Home,
    FileText,
    Settings,
    User,
    Menu,
    X,
    BarChart2,
    Bot,
    LogOut,
    DollarSign,
} from 'lucide-vue-next';

const isCollapsed = ref(false);
const isMobileSidebarOpen = ref(false);

const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
};

const toggleMobileSidebar = () => {
    isMobileSidebarOpen.value = !isMobileSidebarOpen.value;
};

const navItems = [
    { name: 'Home', icon: Home, active: true },
    { name: 'Suggestions', icon: Bot, active: false },
    { name: 'Graphs', icon: BarChart2, active: false },
    { name: 'Settings', icon: Settings, active: false },
];
</script>

<style scoped>
/* Custom scrollbar for Webkit browsers */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #2d3748;
}

::-webkit-scrollbar-thumb {
    background: #4a5568;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #718096;
}

/* Prevent content from being hidden behind the mobile bottom navigation */
@media (max-width: 767px) {
    .pb-16 {
        padding-bottom: 5rem;
    }
}
</style>
