<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<template>
    <div class="home">
        <h1>Welcome to our website!</h1>
        <p>Explore our amazing features and services.</p>
        <div class="buttons">
            <RouterLink to="/auth" loginToggled="true" class="button">Login</RouterLink>
            <RouterLink to="/auth" loginToggled="false" class="button">Register</RouterLink>
        </div>
    </div>
</template>

<style scoped>

.home {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: rgb(31, 150, 248);
    color: white;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

p {
    font-size: 1.5rem;
    margin-bottom: 2rem;
}

.buttons {
    display: flex;
    gap: 1rem;
}

.button {
    padding: 0.75rem 1.5rem;
    background-color: white;
    color: rgb(31, 150, 248);
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    text-decoration: none;
    cursor: pointer;
}

.button:hover {
    background-color: lightblue;
}
</style>