<template>
    <div
        class="flex flex-col min-h-screen bg-gradient-to-tr from-day-gradient-from to-day-gradient-to w-full"
    >
        <main class="flex-1 py-6">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-4">
                <!-- <DashboardFrequencyHistogram /> -->
                <DashboardDaytisticsList data-aos="fade-up" />
            </div>
        </main>
    </div>
</template>

<script lang="ts" setup>
definePageMeta({
    layout: 'dashboard',
    middleware: 'auth',
});

useHead({
    title: 'Daytistics • Dashboard',
});
</script>
