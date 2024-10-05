<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />

    <div id="early-stage" class="flex items-center p-4 text-green-800 rounded-lg bg-green-200" role="alert">
      <svg class="flex-shrink-0 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
        viewBox="0 0 20 20">
        <path
          d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z" />
      </svg>
      <div class="ms-3 text-sm font-medium">
        Welcome to the proof of concept of Daytistics! Thank you for testing it out. We would love to hear your
        <NuxtLink to="/feedback" class="underline">feedback</NuxtLink>.
      </div>
    </div>

    <div class="flex-1">
      <slot />
    </div>
    <Footer />
  </div>
</template>

<script lang="ts" setup>

import { initDismisses } from 'flowbite';


onMounted(() => {
  useAuth().isAuthenticated();
  useUserStore().initUser();
  initDismisses();
});

</script>

<style></style>