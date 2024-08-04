<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<template>
    <div>
        <h1>Die Verifizierung wurden abgewiesen!</h1>
        <p>Bitte versuche es in 5 Minuten erneut!</p>
        <RouterLink to="/auth">Erneut versuchen</RouterLink>
    </div>
</template>

<style scoped>
    div {
        text-align: center;
        margin-top: 50px;
    }

    h1 {
        font-size: 24px;
        color: #333;
    }

    p {
        font-size: 16px;
        color: #666;
        margin-bottom: 20px;
    }

    RouterLink {
        color: #007bff;
        text-decoration: none;
    }
</style>

