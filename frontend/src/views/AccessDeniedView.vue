<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<template>
    <div>
        <h1>Access Denied</h1>
        <p>You are not allowed to access this page.</p>
        <RouterLink to="/">Go back to the home page</RouterLink>
    </div>
</template>