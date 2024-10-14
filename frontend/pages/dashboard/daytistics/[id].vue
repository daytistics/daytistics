<template>
  <DaytisticAddActivityModal @submit="fetchDaytistic" :date="daytistic?.date" />

  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-6 py-8 bg-primary">
        <h1 class="text-3xl font-bold text-white">Daytistic Detail</h1>
        <p class="mt-2 text-lg text-indigo-100">
          {{ new Date(daytistic?.date as string).toLocaleDateString() }}
        </p>
      </div>

      <div class="px-6 py-8">
        <DaytisticWellbeings :daytistic="daytistic as Daytistic" class="mb-12" />
        <DaytisticDiary :daytistic="daytistic as Daytistic" class="mb-12" />
        <DaytisticActivities :daytistic="daytistic as Daytistic" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { Daytistic } from '~/interfaces/daytistics';
import { initModals } from 'flowbite';

const daytistic = ref<Daytistic | null>(null);

const { $api } = useNuxtApp();

async function fetchDaytistic(): Promise<void> {
  const id = useRoute().params.id;

  try {
    const response = await $api(`/api/daytistics/${id}`, {
      server: false,
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }) as Daytistic;

    daytistic.value = response;
  } catch (error) {
    console.error('Error fetching daytistic:', error);
    useRouter().push('/dashboard/');
  }
}

onMounted(async () => {
  initModals();
  await fetchDaytistic();
});
</script>
