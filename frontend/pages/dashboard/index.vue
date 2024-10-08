<template>

  <DashboardAddDaytisticModal @close="initModals" />

  <div class="flex flex-col min-h-screen bg-gray-100">

    <main class="flex-1 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500">Good evening, @{{ userStore.username }}</p>

        <div class="grid grid-cols-4 grid-rows-2 lg:grid-rows-1 lg:grid-cols-5 gap-3 mt-6">
          <div class="col-span-2 row-span-1 lg:col-span-3 w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4">Activity Chart</h2>
            <div class="flex space-x-4 mb-4 border-t border-gray-200 pt-4">
              <select v-model="factor1" class="border rounded p-2">
                <option value="sleep">Sleep</option>
                <option value="exercise">Exercise</option>
                <option value="diet">Diet</option>
              </select>
              <select v-model="factor2" class="border rounded p-2">
                <option value="productivity">Productivity</option>
                <option value="mood">Mood</option>
                <option value="energy">Energy</option>
              </select>
            </div>
            <canvas ref="chartCanvas"></canvas>
          </div>

          <div class="col-span-2 grid-rows-1 w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4">Suggestions</h2>
            <div class="flex flex-col justify-between border-t border-gray-200 pt-4">
              <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam, repellat! Qui nihil commodi saepe quo
                magnam totam culpa! Ratione mollitia nobis ad quam a voluptatum corporis eius numquam, ipsa iusto! Lorem
                ipsum dolor sit, amet consectetur adipisicing elit.
                <br>
                Magnam, tenetur, totam, eveniet deleniti non a
                blanditiis quam laudantium corrupti enim rerum saepe quaerat omnis fuga aspernatur necessitatibus eius
                ea rem.
              </p>
              <div class="flex flex-col items-end gap-3">
                <div class="bg-green-100 rounded-lg p-3 max-w-xs hover:cursor-pointer">
                  <p>Receive a professional analysis</p>
                </div>
                <div class="bg-green-100 rounded-lg p-3 max-w-xs hover:cursor-pointer">
                  <p>Regenerate Analysis</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex flex-row gap-3">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Your Daytistics</h3>
            <button data-modal-target="add-daytistic-modal" data-modal-show="add-daytistic-modal"
              class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out">
              <Plus class="w-5 h-5 mr-1" />
              <span class="text-sm font-medium">Add New</span>
            </button>
          </div>
          <div class="border-t border-gray-200">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex items-center justify-between mb-4">
                <input type="text" placeholder="Search date..."
                  class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md" />
                <button
                  class="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                  Search
                </button>
              </div>
              <ul class="divide-y divide-gray-200">
                <li v-for="(daytistic, index) in daytistics" :key="index" class="py-4 cursor-pointer hover:bg-gray-50">
                  <NuxtLink :to="`/dashboard/daytistics/${daytistic.id}`">
                    <div class="flex items-center space-x-4">
                      <Calendar class="h-6 w-6 text-gray-400" />
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          {{ new Date(daytistic.date).toLocaleDateString() }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ daytistic.total_activities }} Activities / {{ daytistic.total_duration }}
                        </p>
                      </div>
                    </div>
                  </NuxtLink>
                </li>
                <div class="flex justify-center">
                  <span v-show="totalPages <= 0" class="text-lg">
                    We couldn't find any daytistics for you. Why not
                    <button data-modal-target="add-daytistic-modal" data-modal-show="add-daytistic-modal" type="button"
                      class="text-secondary">create</button>
                    one?
                  </span>
                </div>
              </ul>
              <div class=" mt-4 flex items-center justify-between">
                <button :disabled="currentPage === 1" @click="currentPage--"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Previous
                </button>
                <span v-show="totalPages > 0" class="text-sm text-gray-700"> Page {{ currentPage }} of {{
                  totalPages }}
                </span>
                <button :disabled="currentPage === totalPages" @click="currentPage++"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { initDials, initDrawers, initFlowbite, initModals, Modal } from 'flowbite';

const daytistics = ref<Daytistic[] | []>([]);
const userStore = useUserStore();
const auth = useAuth();

const { $api } = useNuxtApp();

import { Plus, PlusCircle, AlertTriangle, BarChart2, Calendar, MessageCircle, Github, Brain, Server, HelpingHandIcon } from 'lucide-vue-next';

const cards = [
  { title: 'Create', description: 'Create a new daytistic, diary entry or AI model.', icon: PlusCircle, implemented: true },
  { title: 'Issues', description: 'Report a bug or submit a feature request.', icon: AlertTriangle, implemented: false },
  { title: 'Personal Analysis', description: 'Let our professionals analyze your data and train models on it.', icon: HelpingHandIcon, implemented: false },
  { title: 'Self-Hosting', description: 'Host your own Daytistics on your own server.', icon: Server, implemented: false },
];

async function listDaytisticsRequest(page: number): Promise<any> {
  return $api(`/api/daytistics/list?page=${page}`, {
    server: false,
    method: 'GET',
  });
}

async function initDaytisticsList(page: number) {
  const response = await listDaytisticsRequest(page);
  console.group('Daytistics');
  console.log(response);
  console.groupEnd();
  daytistics.value = response.items;
  console.log(response.items);
  totalPages.value = Math.ceil(response.count / 5);
}

const currentPage = ref(1);
const totalPages = ref(1);

watch(currentPage, async (newPage) => {

  if (totalPages.value > 0) {
    await initDaytisticsList(newPage);
  }
});


onMounted(async () => {
  await userStore.fetchUser();
  initDaytisticsList(currentPage.value);
  initDrawers();
  initModals();
});




import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';
import type { Daytistic } from '~/interfaces/daytistics';

const factor1 = ref('sleep');
const factor2 = ref('productivity');
const chartCanvas = ref(null);
let chart = null;

const activities = ref(['Exercise', 'Meditation', 'Reading', 'Cooking']);

onMounted(() => {
  createChart();
});

watch([factor1, factor2], () => {
  if (chart) {
    chart.destroy();
  }
  createChart();
});

function createChart() {
  const ctx = chartCanvas.value.getContext('2d');
  chart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: `${factor1.value} vs ${factor2.value}`,
        data: generateRandomData(),
        backgroundColor: 'rgba(75, 192, 192, 0.6)'
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: factor1.value
          }
        },
        y: {
          title: {
            display: true,
            text: factor2.value
          }
        }
      }
    }
  });
}

function generateRandomData() {
  return Array.from({ length: 20 }, () => ({
    x: Math.random() * 10,
    y: Math.random() * 10
  }));
}

</script>

<style></style>