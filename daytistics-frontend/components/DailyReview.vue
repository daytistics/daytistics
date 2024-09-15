<template>
  <div class="flex flex-col text-black bg-card_white shadow-lg rounded-lg p-4">
    <p class="text-3xl font-semibold mb-3">Look back 12 days</p>
    <Tabs v-model:value="tab">
      <TabList class="flex flex-row text-black font-semibold">
        <Tab value="0" class="bg-subcard_white p-2 rounded-md shadow-md" :class="{ 'bg-selected_white': tab == '0' }">
          Rating</Tab>
        <Tab value="1" class="bg-subcard_white p-2 rounded-md shadow-md ml-1">Well-being</Tab>
        <Tab value="2" class="bg-subcard_white p-2 rounded-md shadow-md ml-1">Top 5 activities</Tab>
        <Tab value="3" class="bg-subcard_white p-2 rounded-md shadow-md ml-1">Moment of Happiness</Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="1">
          <div>
            <ul>
              <li>
                <span>
                  Time for me
                  <Rating class="inline-block" v-model="value" :stars="5" readonly />
                </span>
              </li>
              <li>
                <span>
                  Health
                  <Rating v-model="value">
                    <template #onicon>
                      <NuxtImg src="/images/wellbeing_onicon.png" height="24" width="24" />
                    </template>
                    <template #officon>
                      <NuxtImg src="/images/wellbeing_officon.png" height="24" width="24" />
                    </template>
                  </Rating>

                </span>
              </li>
              <li>
                <span>
                  Family & Friends
                  <Rating class="flex flex-row" v-model="value" :stars="5" onicon readonly />
                </span>
              </li>
              <li>
                <span>
                  Work & Productivity
                  <Rating class="inline-block" v-model="value" :stars="5" readonly />
                </span>
              </li>
              <li>
                <span>
                  Happiness
                  <Rating class="inline-block" v-model="value" :stars="5" readonly />
                </span>
              </li>
              <li>
                <span>
                  Recreation
                  <Rating class="inline-block" v-model="value" :stars="5" readonly />
                </span>
              </li>
              <li>
                <span>
                  Gratitute
                  <Rating class="inline-block" v-model="value" :stars="5" readonly />
                </span>
              </li>
            </ul>
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>


    <!-- <Fieldset legend="Moment of happiness">
            <p class="m-0">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua.
            </p>
          </Fieldset> -->
  </div>
</template>

<script lang="ts" setup>
const value = ref(3);
const tab = ref('0');


</script>

<style></style>