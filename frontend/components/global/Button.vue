<template>
    <button
        title="title"
        :type="submittable ? 'submit' : 'button'"
        @click="emit('click')"
        :aria-label="ariaLabel"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-day-secondary hover:bg-day-tertiary"
    >
        <slot></slot>
    </button>
</template>

<script setup lang="ts">
const props = defineProps<{
    title: string;
    submittable?: boolean;
    ariaLabel?: string;
    link?: string;
}>();

const emit = defineEmits(['click']);
</script>
