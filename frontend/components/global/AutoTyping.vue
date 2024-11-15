<template>
    <p>{{ displayedText }}</p>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const texts = [
    'Willkommen zur selbstschreibenden Text-Demo.',
    'Dieser Text schreibt und löscht sich selbst.',
    'Perfekt für dynamische Inhalte.',
];

const displayedText = ref('');
const currentTextIndex = ref(0);
const isDeleting = ref(false);
let typingInterval = null;

const typeText = () => {
    const currentText = texts[currentTextIndex.value];
    const speed = isDeleting.value ? 50 : 100;

    if (!isDeleting.value && displayedText.value === currentText) {
        isDeleting.value = true;
        setTimeout(typeText, 1000);
        return;
    }

    if (isDeleting.value && displayedText.value === '') {
        isDeleting.value = false;
        currentTextIndex.value = (currentTextIndex.value + 1) % texts.length;
        setTimeout(typeText, 500);
        return;
    }

    displayedText.value = isDeleting.value
        ? currentText.substring(0, displayedText.value.length - 1)
        : currentText.substring(0, displayedText.value.length + 1);

    typingInterval = setTimeout(typeText, speed);
};

onMounted(() => {
    typeText();
});

onUnmounted(() => {
    clearTimeout(typingInterval);
});
</script>

<style scoped>
@keyframes blink {
    0%,
    100% {
        opacity: 0;
    }
    50% {
        opacity: 1;
    }
}
.animate-blink {
    animation: blink 0.7s infinite;
}
</style>
