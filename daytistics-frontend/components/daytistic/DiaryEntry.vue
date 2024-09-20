<template>

  <div data-popover id="popover-explanation" role="tooltip"
    class="absolute z-10 invisible inline-block w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
      <h3 class="font-semibold text-gray-900 dark:text-white">Diary</h3>
    </div>
    <div class="px-3 py-2">
      <p>This tab contains the diary entry corresponding to this day.</p>
    </div>
    <div data-popper-arrow></div>
  </div>

  <div class="inline-block flex-col justify-start ">
    <div class="flex flex-row align-middle items-center mb-3">
      <svg class="w-6 h-6 inline text-gray-600 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
        data-popover-target="popover-explanation" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9.529 9.988a2.502 2.502 0 1 1 5 .191A2.441 2.441 0 0 1 12 12.582V14m-.01 3.008H12M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <h1 class="text-3xl font-semibold mb-1 ml-2 mr-60 md:mr-0">Diary
      </h1>
    </div>


    <div class="card lg:min-w-800px lg:max-w-800px">
      <label for="diary-entry" class="block mb-2 text-lg font-bold text-gray-900 dark:text-white">Diary Entry</label>
      <textarea id="diary-entry" maxlength="500"
        class="resize-none block h-36 w-full px-4 py-3 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Write your diary entry..." required></textarea>
    </div>

    <div class="card lg:min-w-800px lg:max-w-800px mt-8">
      <label for="diary-entry" class="block mb-2 text-lg font-bold text-gray-900 dark:text-white">Moment Of
        Happiness</label>
      <textarea id="diary-entry" maxlength="150"
        class="resize-none block w-full px-4 py-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Write your diary entry..." required></textarea>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { initPopovers } from 'flowbite';

const items = ref(Array.from({ length: 7 }, (_, i) => `Item #${i}`));

onMounted(() => {
  initPopovers();
});

</script>

<style></style>