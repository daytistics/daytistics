<template>
    <div class="w-full md:w-1/2 relative">
        <div class="bg-gray-400 p-4 rounded-t-xl">
            <div class="flex space-x-2">
                <div
                    v-for="color in ['bg-red-500', 'bg-yellow-500', 'bg-green-500']"
                    :key="color"
                    :class="[color, 'w-3 h-3 rounded-full']"
                ></div>
            </div>
        </div>
        <div class="bg-gray-300 p-4 rounded-b-xl">
            <slot />
        </div>
    </div>
</template>
