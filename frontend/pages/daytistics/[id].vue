<template>
    <DaytisticAddActivityModal
        @submit="fetchDaytistic"
        :date="daytistic?.date"
    />

    <div
        class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8 w-full bg-gradient-to-t from-primary to-green-300"
    >
        <div
            class="max-w-3xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden"
        >
            <div class="px-6 py-8 bg-gray-50 border-b border-gray-200">
                <h1 class="text-3xl font-bold text-primary">
                    What you did on...
                </h1>
                <p class="mt-2 text-lg text-gray-500">
                    {{
                        new Date(daytistic?.date as string).toLocaleDateString()
                    }}
                </p>
            </div>

            <div class="px-6 py-8">
                <DaytisticWellbeings
                    :daytistic="daytistic as Daytistic"
                    class="mb-12"
                />
                <DaytisticDiary
                    :daytistic="daytistic as Daytistic"
                    class="mb-12"
                />
                <DaytisticActivities :daytistic="daytisticAsDaytistic" />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { Daytistic } from '~/types/daytistics';
import { initModals } from 'flowbite';

const daytistic = ref<Daytistic | null>(null);

// Does only exist to ensure that syntax highlighting works correctly
const daytisticAsDaytistic = computed(() => daytistic.value as Daytistic);

const { $api } = useNuxtApp();

async function fetchDaytistic(): Promise<void> {
    const id = useRoute().params.id;

    try {
        const response = (await $api(`/api/daytistics/${id}`, {
            server: false,
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })) as Daytistic;

        daytistic.value = response;
    } catch (error) {
        console.error('Error fetching daytistic:', error);
        useRouter().push('/');
    }
}

definePageMeta({
    layout: 'dashboard',
});

onMounted(async () => {
    initModals();
    await fetchDaytistic();
});
</script>
