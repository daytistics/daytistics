<template>
    <div class="max-w-3xl mx-auto p-4 sm:p-6 lg:p-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">
            Frequently Asked Questions
        </h2>
        <div class="space-y-4 flex flex-col justify-center items-center">
            <div
                v-for="(item, index) in faqItems"
                :key="index"
                class="border border-gray-200 rounded-xl min-w-[800px]"
            >
                <button
                    @click="toggleItem(index)"
                    class="flex justify-between items-center w-full p-4 text-left focus:outline-none"
                    :aria-expanded="item.isOpen"
                    :aria-controls="`faq-answer-${index}`"
                >
                    <span class="text-lg font-medium text-gray-900">{{ item.question }}</span>
                    <ChevronDownIcon
                        :class="[
                            'w-5 h-5 text-gray-500 transition-transform duration-200',
                            { 'transform rotate-180': item.isOpen },
                        ]"
                    />
                </button>
                <hr />
                <div
                    v-show="item.isOpen"
                    :id="`faq-answer-${index}`"
                    class="px-4 py-4"
                >
                    <p class="text-gray-600">{{ item.answer }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { ChevronDownIcon } from 'lucide-vue-next';

const faqItems = ref([
    {
        question: 'What is Vue.js?',
        answer: 'Vue.js is a progressive JavaScript framework for building user interfaces. It is designed to be incrementally adoptable and can easily scale between a library and a full-featured framework.',
        isOpen: false,
    },
    {
        question: 'How do I install Vue.js?',
        answer: "You can install Vue.js using npm by running 'npm install vue' in your terminal. Alternatively, you can include it via a CDN link in your HTML file.",
        isOpen: false,
    },
    {
        question: 'What are the key features of Vue.js?',
        answer: 'Some key features of Vue.js include its reactive data binding, component-based architecture, virtual DOM for efficient updates, computed properties and watchers, and built-in state management with Vuex.',
        isOpen: false,
    },
    {
        question: 'Is Vue.js suitable for large-scale applications?',
        answer: 'Yes, Vue.js is suitable for large-scale applications. It offers a robust ecosystem with official libraries for routing (Vue Router) and state management (Vuex), making it capable of handling complex application architectures.',
        isOpen: false,
    },
    {
        question: 'How does Vue.js compare to React and Angular?',
        answer: 'Vue.js is often considered easier to learn than React or Angular. It combines the best aspects of both: it uses a virtual DOM like React for performance and has a template-based approach similar to Angular. Vue is more flexible and less opinionated than Angular, and has a smaller learning curve than React.',
        isOpen: false,
    },
]);

const toggleItem = (index) => {
    faqItems.value[index].isOpen = !faqItems.value[index].isOpen;
};
</script>
