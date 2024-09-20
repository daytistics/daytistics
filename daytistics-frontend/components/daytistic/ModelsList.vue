<template>

  <div data-popover id="popover-explanation" role="tooltip"
    class="absolute z-10 invisible inline-block w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
      <h3 class="font-semibold text-gray-900 dark:text-white">Models</h3>
    </div>
    <div class="px-3 py-2">
      <p>This tab contains all models whose training data contains this daytistic.</p>
    </div>
    <div data-popper-arrow></div>
  </div>

  <div class="inline-block align-middle ">
    <div class="flex flex-row align-middle items-center mb-3">
      <svg class="w-6 h-6 inline text-gray-600 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
        data-popover-target="popover-explanation" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9.529 9.988a2.502 2.502 0 1 1 5 .191A2.441 2.441 0 0 1 12 12.582V14m-.01 3.008H12M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <h1 class="text-3xl font-semibold mb-1 ml-2">Models
      </h1>
    </div>

    <div class="grid grid-cols-1 grid-rows-20 card p-4 lg:min-w-800px lg:max-w-800px">
      <form class="max-w-md mx-auto flex items-center space-x-2">


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
            placeholder="Search model..." required />
        </div>

        <button type="submit" class="button">
          Search
        </button>
      </form>
      <ul class="row-span-17 flex flex-col p-4 gap-2 lg:min-h-690px lg:max-h-690px">
        <li v-for="number in [0, 1, 2, 3, 4, 5, 6]" class="border-gray-400 flex flex-row mb-2"
          data-modal-target="edit-activity-modal" data-modal-show="edit-activity-modal">
          <div
            class="select-none cursor-pointer bg-gray-100 rounded-md flex flex-1 items-center p-4  transition duration-500 ease-in-out transform hover:-translate-y-1 hover:shadow-lg">
            <div class="flex flex-col rounded-md w-10 h-10 bg-gray-200 justify-center items-center mr-4">
              <svg version="1.0" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                class="w-6 h-6 text-gray-400 dark:text-white" viewBox="0 0 24 24" xml:space="preserve" stroke="none">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                  <g id="Guides">
                    <g id="_x32_0_px_2_"> </g>
                    <g id="_x32_0px"> </g>
                    <g id="_x34_0px"> </g>
                    <g id="_x34_4_px"> </g>
                    <g id="_x34_8px">
                      <g id="_x31_6px"> </g>
                      <g id="square_4px">
                        <g id="_x32_8_px">
                          <g id="square_4px_2_"> </g>
                          <g id="square_4px_3_"> </g>
                          <g id="square_4px_1_"> </g>
                          <g id="_x32_4_px_2_"> </g>
                          <g id="_x31_2_px"> </g>
                        </g>
                      </g>
                    </g>
                    <g id="Icons"> </g>
                    <g id="_x32_0_px"> </g>
                    <g id="square_6px">
                      <g id="_x31_2_PX"> </g>
                    </g>
                    <g id="_x33_6_px">
                      <g id="_x33_2_px">
                        <g id="_x32_8_px_1_">
                          <g id="square_6px_1_"> </g>
                          <g id="_x32_0_px_1_">
                            <g id="_x31_2_PX_2_"> </g>
                            <g id="_x34_8_px">
                              <g id="_x32_4_px"> </g>
                              <g id="_x32_4_px_1_"> </g>
                            </g>
                          </g>
                        </g>
                      </g>
                    </g>
                    <g id="_x32_0_px_3_"> </g>
                    <g id="_x32_0_px_4_"> </g>
                    <g id="New_Symbol_8">
                      <g id="_x32_4_px_3_"> </g>
                    </g>
                  </g>
                  <g id="Artboard"> </g>
                  <g id="Free_Icons">
                    <g>
                      <polygon style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;"
                        points="6,21.5 0.5,12 6,2.5 18,2.5 23.5,12 18,21.5 "></polygon>
                      <polygon style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;"
                        points="23.5,12 16,7.5 6,2.5 5,13.5 6,21.5 16.5,19.5 "></polygon>
                      <polygon style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;"
                        points="16,7.5 5,13.5 16.5,19.5 "></polygon>
                      <line style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;" x1="18"
                        y1="21.5" x2="16.5" y2="19.5"></line>
                      <line style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;" x1="0.5"
                        y1="12" x2="5" y2="13.5"></line>
                      <line style="fill:none;stroke:currentColor;stroke-linejoin:round;stroke-miterlimit:10;" x1="18"
                        y1="2.5" x2="16" y2="7.5"></line>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
            <div class="flex-1 pl-1 mr-16">
              <div class="font-medium">Trained on 01/21/2008</div>
              <div class="text-gray-600 text-sm">100.000 records | 78% accuracy</div>
            </div>
          </div>
        </li>
      </ul>
      <div class="flex justify-center">
        <Paginator />
      </div>
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