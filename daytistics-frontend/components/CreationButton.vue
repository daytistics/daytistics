<template>

  <!-- <Dialog v-model:visible="showDaytisticsCreationMenu" :draggable="false" modal header="Create Daytistic">
    <div class="flex items-center gap-4 mb-8">
      <p class="font-semibold">Date</p>
      <DatePicker v-model="date" />
    </div>
    <div class="flex items-center gap-4 mb-8">
      <p class="font-semibold">Important</p>
      <Checkbox v-model="checked" :binary="true" />
    </div>
    <div class="flex justify-end gap-2">
      <Button type="button" label="Save" @click="showDaytisticsCreationMenu = false"></Button>
    </div>

  </Dialog> -->

  <DaytisticsCreationDialog :visible="showDaytisticsCreationDialog"
    @update:visible="showDaytisticsCreationDialog = $event" />

  <div class="fixed bottom-5 right-5 flex flex-col justify-center items-end gap-4 text-black">
    <div v-show="showingOptions" class="flex flex-col justify-center items-end gap-4">
      <div class="flex justify-center items-center gap-3 mr-2.5">
        <p class="font-semibold">
          Daytistic
        </p>
        <div @click="showDaytisticsCreationDialog = true"
          class="bg-green-600 p-3 rounded-full shadow-slate-400 hover:cursor-pointer hover:bg-green-700 shadow-lg">
          <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
              <g clip-path="url(#clip0_429_11003)">
                <path d="M12 20V4L9 7" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"
                  stroke-linejoin="round">
                </path>
              </g>
              <defs>
                <clipPath id="clip0_429_11003">
                  <rect width="24" height="24" fill="white"></rect>
                </clipPath>
              </defs>
            </g>
          </svg>
        </div>
      </div>
      <div class="flex justify-center items-center gap-3 mr-2.5">
        <p class="font-semibold">
          Diary Entry
        </p>
        <div @click="showDiaryEntryCreationDialog = true"
          class="bg-green-600 p-3 rounded-full shadow-slate-400 hover:cursor-pointer hover:bg-green-700 shadow-lg">
          <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
              <g clip-path="url(#clip0_429_10997)">
                <path
                  d="M8 8C8 6.97631 8.39052 5.95262 9.17157 5.17157C10.7337 3.60947 13.2663 3.60947 14.8284 5.17157C16.3905 6.73366 16.3905 9.26632 14.8284 10.8284L9.17157 16.4853C8.42143 17.2354 8 18.2528 8 19.3137L8 20L16 20"
                  stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path>
              </g>
              <defs>
                <clipPath id="clip0_429_10997">
                  <rect width="24" height="24" fill="white"></rect>
                </clipPath>
              </defs>
            </g>
          </svg>
        </div>
      </div>
      <div class="flex justify-center items-center gap-3 mr-2.5">
        <p class="font-semibold">
          Prediction Model
        </p>
        <div @click="showModelCreationDialog = true"
          class="bg-green-600 p-3 rounded-full shadow-slate-400 hover:cursor-pointer hover:bg-green-700 shadow-lg">
          <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
              <g clip-path="url(#clip0_429_10996)">
                <path
                  d="M8 19.0004C8.83566 19.6281 9.87439 20 11 20C13.7614 20 16 17.7614 16 15C16 12.2386 13.7614 10 11 10L16 4H8"
                  stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path>
              </g>
              <defs>
                <clipPath id="clip0_429_10996">
                  <rect width="24" height="24" fill="white"></rect>
                </clipPath>
              </defs>
            </g>
          </svg>
        </div>
      </div>
    </div>

    <div @click="showingOptions = !showingOptions"
      class="bg-green-600 p-3 rounded-full shadow-lg shadow-slate-400 hover:cursor-pointer hover:-translate-y-1 transition ease-in-out">
      <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
        :class="{ 'rotate-45': showingOptions }">
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
const showingOptions = ref(false);
const showDaytisticsCreationDialog = ref(false);
const showDiaryEntryCreationDialog = ref(false);
const showModelCreationDialog = ref(false);
const date = ref(new Date());
const checked = ref(false);

function handleSaveDaytistic() {
  console.log('Daytistic saved');
}

</script>

<style></style>