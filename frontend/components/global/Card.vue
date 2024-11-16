<template>
    <div
        class="bg-gray-100 p-5 rounded-xl border-gray-200 border"
        :class="{
            'hover:cursor-pointer': clickable,
        }"
        @click="clickable ? emit('click') : null"
    >
        <slot></slot>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    clickable?: boolean;
}>();

const emit = defineEmits(['click']);
</script>
