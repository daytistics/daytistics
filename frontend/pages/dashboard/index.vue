<template>

  <DashboardAddDaytisticModal @close="initModals" />

  <div class="flex flex-col min-h-screen bg-gray-100">

    <main class="flex-1 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500">{{ getGreeting() }}, @{{ userStore.username }}</p>

        <div class="grid grid-cols-2 grid-rows-2 lg:grid-rows-1 lg:grid-cols-5 gap-3 mt-6">
          <DashboardGraphContainer class="col-span-2 row-span-1 lg:col-span-3" />
          <DashboardChatInterface class="col-span-2 grid-rows-1" />
        </div>

        <DashboardDaytisticsList />


      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { getGreeting } from '~/utils/misc';

const userStore = useUserStore();

onMounted(async () => {
  await userStore.fetchUser();
});
</script>
