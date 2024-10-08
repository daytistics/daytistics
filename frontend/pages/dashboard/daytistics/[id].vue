<template>
  <DaytisticAddActivityModal @submit="fetchDaytistic" :date="daytistic?.date" />

  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-6 py-8 bg-gradient-to-tr from-primary to-secondary">
        <h1 class="text-3xl font-bold text-white">Daytistic Detail</h1>
        <p class="mt-2 text-lg text-indigo-100">
          <!-- {{ readableDateFromUTC(daytistic?.date) }} -->
          {{ new Date(daytistic?.date as string).toLocaleDateString() }}
        </p>
      </div>

      <div class="px-6 py-8">
        <section aria-labelledby="wellbeing-ratings-title" class="mb-12">
          <h2 id="wellbeing-ratings-title" class="text-2xl font-semibold text-gray-900 mb-6">
            Well-being Ratings
          </h2>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div v-for="wellbeing in daytistic?.wellbeing" :key="daytistic?.wellbeing.id"
              class="bg-gray-50 p-4 rounded-lg shadow-sm">
              <h3 class="text-sm font-medium text-gray-500 mb-2">
                {{ wellbeing.name }}
              </h3>
              <div class="flex items-center">
                <div class="flex">
                  <Star v-for="star in 5" :key="star" @click="" />
                </div>
                <span class="ml-2 text-sm text-gray-700">{{ wellbeing.rating }}/5</span>
              </div>
            </div>
          </div>
        </section>

        <section aria-labelledby="diary-entry-title" class="mb-12">
          <div class="flex items-center mb-6">
            <h2 id="diary-entry-title" class="text-2xl font-semibold text-gray-900 mr-4">
              Diary Entry
            </h2>
            <button @click="toggleDiaryEdit"
              class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out"
              :aria-label="isEditingDiary
                ? 'Cancel editing'
                : 'Edit diary entry'
                ">
              <component :is="isEditingDiary ? X : Edit2" class="w-5 h-5 mr-1" />
              <span class="text-sm font-medium">{{
                isEditingDiary ? 'Cancel' : 'Edit'
                }}</span>
            </button>
          </div>
          <div class="bg-gray-50 p-6 rounded-lg shadow-sm">
            <div v-if="!isEditingDiary" class="prose max-w-none">
              <p class="text-gray-700">
                {{ daytistic?.diary.entry }}
              </p>
              <div class="mt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-3">
                  Moment of Happiness
                </h3>
                <p class="text-gray-700">
                  {{ daytistic?.diary.moment_of_happiness }}
                </p>
              </div>
            </div>
            <div v-else>
              <label for="diary-entry" class="block text-sm font-medium text-gray-700 mb-2">Diary Entry</label>
              <textarea id="diary-entry" v-model="editedDiaryEntry"
                class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                rows="4"></textarea>
              <label for="moment-of-happiness" class="block text-sm font-medium text-gray-700 mb-2">Moment of
                Happiness</label>
              <textarea id="moment-of-happiness" v-model="editedMomentOfHappiness"
                class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                rows="2"></textarea>
              <button @click="saveDiaryChanges"
                class="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                Save Changes
              </button>
            </div>
          </div>
        </section>

        <section aria-labelledby="activities-title">
          <div class="flex items-center mb-6">
            <h2 id="diary-entry-title" class="text-2xl font-semibold text-gray-900 mr-4">
              Activities
            </h2>
            <button data-modal-target="add-activity-modal" data-modal-show="add-activity-modal"
              class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out">
              <Plus class="w-5 h-5 mr-1" />
              <span class="text-sm font-medium">Add New</span>
            </button>
          </div>
          <ul class="bg-gray-50 rounded-lg shadow-sm overflow-hidden">
            <li v-for="(activity, index) in daytistic?.activities" :key="activity.id" class="group"
              @click="viewActivityDetails(activity)">
              <div
                class="px-6 py-4 flex items-center justify-between hover:bg-gray-100 transition duration-150 ease-in-out cursor-pointer"
                :class="{
                  'border-t border-gray-200': index !== 0,
                }">
                <div>
                  <p
                    class="text-lg font-medium text-gray-900 group-hover:text-indigo-600 transition duration-150 ease-in-out">
                    {{ activity.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{
                      formatTimeWindow(
                        activity.start_time,
                        activity.end_time
                      )
                    }}
                  </p>
                </div>
                <div class="flex items-center">
                  <p class="text-sm font-medium text-gray-900 mr-2">
                    {{ formatDuration(activity.duration) }}
                  </p>
                  <ChevronRight
                    class="w-5 h-5 text-gray-400 group-hover:text-indigo-600 transition duration-150 ease-in-out" />
                </div>
              </div>
            </li>
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Star, Edit2, ChevronRight, X, Plus } from 'lucide-vue-next';
import type { Daytistic } from '~/interfaces/daytistics';
import { initModals } from 'flowbite';

const daytistic = ref<Daytistic | null>(null);
const isEditingDiary = ref(false);
const editedDiaryEntry = ref(daytistic.value?.diary.entry);
const editedMomentOfHappiness = ref(daytistic.value?.diary.moment_of_happiness);
const selectedActivity = ref(null);
const auth = useAuth();
const { $api } = useNuxtApp();

async function fetchDaytistic(): Promise<Daytistic | any> {
  const id = useRoute().params.id;

  try {
    return await $api(`/api/daytistics/${id}`, {
      server: false,
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }) as Daytistic;
  } catch (error) {
    console.error('Error fetching daytistic:', error);
    useRouter().push('/dashboard/');
  }
}


const formatTimeWindow = (startIso: string, endIso: string) => {
  const startTime = new Date(startIso).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
  const endTime = new Date(endIso).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
  return `${startTime} - ${endTime}`;
};

const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
};

const toggleDiaryEdit = () => {
  if (isEditingDiary.value) {
    // Cancel editing
    editedDiaryEntry.value = daytistic.value?.diary.entry;
    editedMomentOfHappiness.value = daytistic.value?.diary.moment_of_happiness;
  }
  isEditingDiary.value = !isEditingDiary.value;
};

const saveDiaryChanges = () => {
  // TODO: Save changes to the server
  isEditingDiary.value = false;
};

const viewActivityDetails = (activity) => {
  selectedActivity.value = activity;
};

onBeforeMount(async () => {


  initModals();
  const response: Daytistic = await fetchDaytistic();
  console.debug("Daytistic", response);
  daytistic.value = response;
  console.debug("Daytistic", daytistic.value);
});
</script>
