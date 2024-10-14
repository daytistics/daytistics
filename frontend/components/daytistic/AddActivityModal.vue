<template>
  <div id="add-activity-modal" tabindex="-1" aria-hidden="true"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Add New Activity
          </h3>
          <button type="button" @click="useModal().closeModal"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>

        <!-- Modal body -->
        <form class="p-4 md:p-5" @submit.prevent="form.submit">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label for="type" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">What activity did
                you do that day?</label>
              <select id="activity-type" v-model="form.activityType.value" required
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500">
                <option v-for="activity in activities" :key="activity.id" :value="activity.id">
                  {{ activity.name }}
                </option>
              </select>
            </div>
            <div>
              <label for="start-time" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Start
                time:</label>
              <div class="relative">
                <div class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none">
                  <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd"
                      d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z"
                      clip-rule="evenodd" />
                  </svg>
                </div>
                <input type="time" id="start-time" v-model="form.startTime.value"
                  class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
                  min="00:00" max="23:59" required />
              </div>
            </div>
            <div>
              <label for="end-time" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">End
                time:</label>
              <div class="relative">
                <div class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none">
                  <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd"
                      d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z"
                      clip-rule="evenodd" />
                  </svg>
                </div>
                <input type="time" id="end-time" v-model="form.endTime.value"
                  class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
                  :min="form.startTime as unknown as string" max="23:59" required />
              </div>
            </div>
          </div>
          <p id="activity-error" class="text-red-500 text-sm mb-4">{{ form.errorMessage }}</p>
          <div class="flex justify-end md:justify-start">
            <button type="submit" class="inline-flex button bg-secondary hover:bg-secondary-dark items-center">
              <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                  clip-rule="evenodd"></path>
              </svg>
              Add activity
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { initModals, Modal } from 'flowbite';
import type { ActivityType } from '~/interfaces/activities';

const emit = defineEmits(['submit']);

const form = useForm();
const { activities } = useActivitiesAPI();

onMounted(() => {
  initModals();
});

function useForm() {

  const { add } = useActivitiesAPI();

  const activityType = ref<number>(0);
  const startTime = ref<string>('00:00');
  const endTime = ref<string>('00:00');
  const errorMessage = ref<string>('');

  const submit = async () => {
    const startTimeString = convert24toMinutes(startTime.value);
    const endTimeString = convert24toMinutes(endTime.value);
    await add(startTimeString, endTimeString);
    useModal().closeModal();
  };

  const setError = (message: string) => {
    errorMessage.value = message;
  };

  return { submit, setError, activityType, startTime, endTime, errorMessage };
}

function useModal() {
  const modal = new Modal(document.getElementById('add-activity-modal'));

  const closeModal = () => {
    modal?.hide();
  };

  return { closeModal };
}

function useActivitiesAPI() {
  const activities = ref<ActivityType[]>([]);
  const { $api } = useNuxtApp();

  const add = async (startTime: number, endTime: number) => {
    const id = useRoute().params.id;
    try {
      await $api(`/api/daytistics/${id}/add-activity`, {
        server: false,
        method: 'POST',
        body: {
          id: form.activityType.value,
          start_time: startTime,
          end_time: endTime,
        },
        onResponse: ({ request, response, options }) => {
          if (response.status === 201) {
            emit('submit');
            useModal().closeModal();
          }
        },
        onResponseError: ({ request, response, options }) => {
          form.setError(response._data.detail);
        },
      });

    } catch (error) {
      console.error('Error creating activity:', error);
    }
  };

  const fetch = async () => {
    try {
      await $api(`/api/activities/`, {
        server: false,
        method: 'GET',

        onResponse: async ({ request, response, options }) => {
          activities.value = response._data;
        },

        onResponseError: ({ request, response, options }) => {
          console.error('Error fetching activities:', response);
        }
      });

    } catch (error) {
      console.error('Error fetching activities:', error);
    }
  };

  onMounted(async () => {
    initModals();
    await fetch();
  });

  return { add, fetch, activities };
}
</script>

<style></style>