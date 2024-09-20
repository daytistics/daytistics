<template>

  <CreationModal />

  <div class="flex flex-col min-h-screen bg-gray-100">

    <main class="flex-1 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500">Good evening, @{{ username }}</p>

        <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="(card, index) in cards" :key="index" @click="handleCardClick(index)"
            class="bg-white overflow-hidden shadow rounded-lg cursor-pointer hover:shadow-md transition-shadow duration-300">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <component :is="card.icon" class="h-6 w-6 text-gray-400" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      {{ card.title }}
                    </dt>
                    <dd class="mt-1 text-sm text-gray-900">
                      {{ card.description }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 grid gap-5 sm:grid-cols-2">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Join our community!</h3>
              <div class="mt-5">
                <NuxtLink to="https://discord.gg/ccud6VkTv8" target="_blank"
                  class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                  <MessageCircle class="mr-2 h-5 w-5" />
                  Join Discord
                </NuxtLink>
              </div>
            </div>
          </div>
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Contribute to our project!</h3>
              <div class="mt-5">
                <NuxtLink to="https://github.com/daytistics" target="_blank"
                  class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-900">
                  <Github class="mr-2 h-5 w-5" />
                  Contribute on GitHub
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Your Daytistics</h3>
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
                <li v-for="(day, index) in displayedDays" :key="index" class="py-4 cursor-pointer hover:bg-gray-50">
                  <NuxtLink to="/dashboard/daytistics/{{ day.id }}">
                    <div class="flex items-center space-x-4">
                      <Calendar class="h-6 w-6 text-gray-400" />
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">
                          {{ day.date }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                          {{ day.activities }} Activities / {{ day.duration }}
                        </p>
                      </div>
                    </div>
                  </NuxtLink>
                </li>
              </ul>
              <div class="mt-4 flex items-center justify-between">
                <button :disabled="currentPage === 1" @click="currentPage--"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Previous
                </button>
                <span class="text-sm text-gray-700">
                  Page {{ currentPage }} of {{ totalPages }}
                </span>
                <button :disabled="currentPage === totalPages" @click="currentPage++"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Trained AI Models</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">AI models trained on your Daytistics data</p>
          </div>
          <div class="border-t border-gray-200">
            <ul class="divide-y divide-gray-200">
              <li v-for="(model, index) in aiModels" :key="index"
                class="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer" @click="handleModelClick(model)">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="flex-shrink-0">
                      <Brain class="h-6 w-6 text-indigo-600" />
                    </div>
                    <div class="ml-4">
                      <h4 class="text-lg font-medium text-gray-900">{{ model.name }}</h4>
                      <p class="text-sm text-gray-500">{{ model.description }}</p>
                    </div>
                  </div>
                  <div class="ml-2 flex-shrink-0 flex">
                    <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      :class="model.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'">
                      {{ model.status }}
                    </p>
                  </div>
                </div>
                <div class="mt-2 sm:flex sm:justify-between">
                  <div class="sm:flex">
                    <p class="flex items-center text-sm text-gray-500">
                      <Calendar class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                      Trained on: {{ model.trainedOn }}
                    </p>
                  </div>
                  <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                    <BarChart2 class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                    Accuracy: {{ model.accuracy }}
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { initDials, initDrawers, initFlowbite, initModals, Modal } from 'flowbite';

const greeting = ref<string>(useUtils().getGreeting());
const username = ref<string>('User');

import { Layers, PlusCircle, AlertTriangle, BarChart2, Calendar, MessageCircle, Github, Brain, Server } from 'lucide-vue-next'

const cards = [
  { title: 'Create', description: 'Create a new daytistic, diary entry or AI model', icon: PlusCircle },
  { title: 'Issues', description: 'Report a bug or submit a feature request', icon: AlertTriangle },
  { title: 'Self-Hosting', description: 'Host your own Daytistics on your own server.', icon: Server },
  { title: 'Stats', description: 'See what you have achieved so far on Daytistic', icon: BarChart2 },
]

const days = [
  { date: '21.01.2008', activities: 12, duration: '23h 30m' },
  { date: '22.01.2008', activities: 8, duration: '18h 45m' },
  { date: '23.01.2008', activities: 15, duration: '22h 15m' },
  { date: '24.01.2008', activities: 10, duration: '20h 00m' },
  { date: '25.01.2008', activities: 14, duration: '21h 30m' },
  { date: '26.01.2008', activities: 9, duration: '19h 15m' },
  { date: '27.01.2008', activities: 11, duration: '20h 45m' },
  { date: '28.01.2008', activities: 13, duration: '22h 00m' },
  { date: '29.01.2008', activities: 7, duration: '17h 30m' },
  { date: '30.01.2008', activities: 16, duration: '23h 45m' },
]

const aiModels = [
  { name: 'Predictor', description: 'Predicts your well-being on a hypothetical day', status: 'Active', trainedOn: '2023-05-15', accuracy: '89%' },
  { name: 'Suggestor', description: 'Suggests optimal schedules for maximum productivity', status: 'Training', trainedOn: '2023-06-01', accuracy: '78%' },
]

const currentPage = ref(1)
const itemsPerPage = 5

const totalPages = computed(() => Math.ceil(days.length / itemsPerPage))

const displayedDays = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return days.slice(start, end)
})

const handleCardClick = (title: number) => {
  switch (title) {
    case 0:
      const modal = new Modal(document.getElementById('creation-modal'));
      modal.show();
      break;

    default:
      break;
  }
}

const handleModelClick = (model) => {
  console.log(`Clicked on AI model: ${model.name}`)
  // Add your logic here for handling AI model clicks
}

onBeforeMount(async () => {
  if (!await useUser().isAuthenticated()) {
    useRouter().push('/login');
  }
})

onMounted(async () => {

  getModel();

  initDrawers();
  initModals();
})

async function getModel() {
  const model: any = await useUser().getModel();
  console.log(model);
  username.value = model.username;
}

</script>

<style></style>