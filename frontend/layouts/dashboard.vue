<template>
    <ErrorDialog />
    <InfoDialog />

    <div class="flex flex-col min-h-screen">
        <div class="flex flex-row">
            <Sidebar />

            <slot />
        </div>
    </div>
</template>

<script lang="ts" setup>
onMounted(() => {
    const { update } = useUserStore();
    update();
});
</script>
