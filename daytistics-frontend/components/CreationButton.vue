<template>

  <USlideover v-model="isOpen">
    <h1 class="text-2xl font-semibold text-white">What do you want to create?</h1>
    <div class="p-4 flex-1">
      <UButton color="emerald" variant="solid">Button</UButton>
    </div>
  </USlideover>

  <div>
    <div @click="isOpen = !isOpen"
      class="fixed bottom-5 right-5 bg-green-600 p-3 rounded-full shadow-lg shadow-slate-400 hover:cursor-pointer hover:-translate-y-1 transition ease-in-out">
      <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
        <g id="SVGRepo_iconCarrier">
          <path d="M4 12H20M12 4V20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          </path>
        </g>
      </svg>
    </div>
  </div>
</template>

<script lang="ts" setup>
const isOpen = ref(false);
</script>

<style></style>