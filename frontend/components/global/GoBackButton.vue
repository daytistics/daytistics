<template>
    <div class="flex flex-row">
        <NuxtLink
            :to="to"
            class="text-white font-bold text-lg rounded-lg flex flex-row justify-center items-center gap-2 hover:translate-x-1 transition duration-200"
        >
            <CircleArrowLeft class="w-16 h-auto" />
        </NuxtLink>
    </div>
</template>

<script setup lang="ts">
import { CircleArrowLeft } from 'lucide-vue-next';

defineProps<{
    to: string;
}>();
</script>
