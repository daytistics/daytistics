<template>

  <div data-popover id="popover-explanation" role="tooltip"
    class="absolute z-10 invisible inline-block w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
      <h3 class="font-semibold text-gray-900 dark:text-white">Activities</h3>
    </div>
    <div class="px-3 py-2">
      <p>This tab contains all the activities you performed that day.</p>
    </div>
    <div data-popper-arrow></div>
  </div>

  <div class="inline-block align-middle w-full">
    <div class="flex flex-row align-middle items-center mb-3">
      <svg class="w-6 h-6 inline text-gray-600 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
        data-popover-target="popover-explanation" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9.529 9.988a2.502 2.502 0 1 1 5 .191A2.441 2.441 0 0 1 12 12.582V14m-.01 3.008H12M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <h1 class="text-3xl font-semibold mb-1 ml-2">Activities
      </h1>
    </div>

    <div class="grid grid-cols-1 grid-rows-20 card p-4 lg:min-w-800px lg:max-w-800px">
      <form class="max-w-md mx-auto flex items-center space-x-2">

        <button type="button" class="inline-flex button items-center p-2.5" data-modal-show="add-activity-modal"
          data-modal-target="add-activity-modal">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clip-rule="evenodd"></path>
          </svg>
        </button>

        <div class="relative flex-grow">
          <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
              fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>
          </div>
          <input type="search" id="default-search"
            class="block w-full px-4 py-3 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search activity..." required />
        </div>

        <button type="submit" class="button hidden md:inline">
          Search
        </button>

        <button type="submit" class="button inline-flex md:hidden p-2.5 justify-center items-center">
          <svg class="w-6 h-6 text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
            fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-width="2"
              d="m21 21-3.5-3.5M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z" />
          </svg>
        </button>
      </form>
      <ul class="row-span-17 flex flex-col p-4 gap-2 lg:min-h-690px lg:max-h-690px">
        <li v-for="number in [0, 1, 2, 3, 4, 5, 6]" class="border-gray-400 flex flex-row mb-2"
          data-modal-target="edit-activity-modal" data-modal-show="edit-activity-modal">
          <div
            class="select-none cursor-pointer bg-gray-100 rounded-md flex flex-1 items-center p-4  transition duration-500 ease-in-out transform hover:-translate-y-1 hover:shadow-lg">
            <div class="flex flex-col rounded-md w-10 h-10 bg-gray-200 justify-center items-center mr-4">
              <svg class="w-6 h-6 text-gray-400 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd"
                  d="M5 5a1 1 0 0 0 1-1 1 1 0 1 1 2 0 1 1 0 0 0 1 1h1a1 1 0 0 0 1-1 1 1 0 1 1 2 0 1 1 0 0 0 1 1h1a1 1 0 0 0 1-1 1 1 0 1 1 2 0 1 1 0 0 0 1 1 2 2 0 0 1 2 2v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a2 2 0 0 1 2-2ZM3 19v-7a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Zm6.01-6a1 1 0 1 0-2 0 1 1 0 0 0 2 0Zm2 0a1 1 0 1 1 2 0 1 1 0 0 1-2 0Zm6 0a1 1 0 1 0-2 0 1 1 0 0 0 2 0Zm-10 4a1 1 0 1 1 2 0 1 1 0 0 1-2 0Zm6 0a1 1 0 1 0-2 0 1 1 0 0 0 2 0Zm2 0a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z"
                  clip-rule="evenodd" />
              </svg>
            </div>
            <div class="flex-1 pl-1 mr-16">
              <div class="font-medium">Swimming</div>
              <div class="text-gray-600 text-sm">23h 30m</div>
            </div>
          </div>
        </li>
      </ul>
      <div class="flex justify-center">
        <Paginator />
      </div>
    </div>
  </div>

  <DaytisticAddActivityModal />
  <DaytisticEditActivityModal />
</template>

<script lang="ts" setup>
import { initPopovers } from 'flowbite';

const items = ref(Array.from({ length: 7 }, (_, i) => `Item #${i}`));

onMounted(() => {
  initPopovers();
});

</script>

<style></style>