<template>
    <div
        class="flex flex-col min-h-screen bg-gradient-to-t from-primary to-green-300 w-full"
    >
        <main class="flex-1 py-6">
            <div
                class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-4"
            >
                <DashboardFrequencyHistogram />
                <DashboardDaytisticsList />
            </div>
        </main>
    </div>
</template>

<script lang="ts" setup>
const userStore = useUserStore();

definePageMeta({
    layout: 'dashboard',
});

onMounted(async () => {
    await userStore.fetchUser();
});
</script>
