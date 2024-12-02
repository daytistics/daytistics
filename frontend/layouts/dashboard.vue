<template>
    <ErrorDialog />
    <InfoDialog />

    <div class="flex flex-col min-h-screen">
        <div class="flex flex-row">
            <DashboardSideBar />

            <slot />
        </div>
    </div>
</template>

<script lang="ts" setup></script>
