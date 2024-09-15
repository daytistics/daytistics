<template>
  <div class="inline-block align-middle bg-card_white shadow-lg rounded-lg">
    <div class="grid grid-cols-1 grid-rows-20">
      <ul v-for="number in [0, 1, 2, 3, 4, 5]" class="row-span-17 flex flex-col p-4">
        <li class="border-gray-400 flex flex-row mb-2">
          <div
            class="select-none cursor-pointer bg-gray-200 rounded-md flex flex-1 items-center p-4  transition duration-500 ease-in-out transform hover:-translate-y-1 hover:shadow-lg">
            <div class="flex flex-col rounded-md w-10 h-10 bg-gray-300 justify-center items-center mr-4">?</div>
            <div class="flex-1 pl-1 mr-16">
              <div class="font-medium">21.01.2008</div>
              <div class="text-gray-600 text-sm">12 Activities / 23h 30m</div>
            </div>
          </div>
        </li>
      </ul>
      <Paginator :rows="10" :totalRecords="120" :rowsPerPageOptions="[10, 20, 30]" class="row-span-3"></Paginator>
    </div>
  </div>
</template>

<script lang="ts" setup>
const items = ref(Array.from({ length: 7 }, (_, i) => `Item #${i}`));
</script>

<style></style>