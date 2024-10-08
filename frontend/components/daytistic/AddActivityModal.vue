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
          <button type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-toggle="add-activity-modal">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>

        <!-- Modal body -->
        <form class="p-4 md:p-5" @submit.prevent="handleSubmit">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label for="type" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">What activity did
                you do that day?</label>
              <select id="activity-type" v-model="activityType" required
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500">
                <option value="" disabled selected>Select an activity</option>
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
                <input type="time" id="start-time" v-model="startTime"
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
                <input type="time" id="end-time" v-model="endTime"
                  class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
                  :min="startTime" max="23:59" value="00:00" required />
              </div>
            </div>
          </div>
          <p id="activity-error" class="text-red-500 text-sm mb-4">{{ errorMessage }}</p>
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
import type { ActivityType, ActivityEntry } from '~/interfaces/activities';
import { convertToUTC } from '~/utils/time';

const { $api } = useNuxtApp();

const activities = ref<ActivityType[]>([]);
const activityType = ref<number>(0);
const startTime = ref<string>('00:00');
const endTime = ref<string>('00:00');
const errorMessage = ref<string>('');
const modalElement = document.getElementById('add-activity-modal');

// Receiving props
const props = defineProps(['date']);

/**
 * Converts time into the according time of the date including timezone
 * @param time Time in HH:MM format
 * @param date Date in ISO format
 * @example convertTimeToIsoString('12:00', '2008-01-21T00:00:00+01:00') => '2008-01-21T12:00:00+01:00'
 */
function convertTimeToIsoString(time: string, date: string): string {
  // Extract hours and minutes from the time string
  const [hours, minutes] = time.split(':').map(Number);

  // Create a new Date object based on the ISO date
  const isoDate = new Date(date);

  // Adjust the date's hours and minutes while considering the timezone
  const timezoneOffset = isoDate.getTimezoneOffset();

  // Set the hours and minutes
  isoDate.setUTCHours(hours + timezoneOffset / 60);
  isoDate.setUTCMinutes(minutes);

  // Return the ISO string in the required format
  return isoDate.toISOString().replace('Z', date.slice(-6));
}

async function handleSubmit() {
  startTime.value = convertTimeToIsoString(startTime.value, props.date);
  endTime.value = convertTimeToIsoString(endTime.value, props.date);

  await addActivity();
}


// Activity fetching specific
const { fetch: fetchActivities } = useActivities();


// Activity adding specific
const emit = defineEmits(['submit']);
const { addNew: addActivity } = useActivities();


// Modal specific
function closeModal() {
  const modal = new Modal(modalElement);
  modal.hide();
}

onMounted(() => {
  initModals();
  fetchActivities();
});

// Reusable composables
function useActivities() {
  {
    const addNew = async () => {
      const id = useRoute().params.id;
      try {
        await $api(`/api/daytistics/${id}/add-activity/`, {
          server: false,
          method: 'POST',
          body: {
            id: activityType.value,
            start_time: convertToUTC(startTime.value),
            end_time: convertToUTC(endTime.value),
          },
          onResponseError: ({ request, response, options }) => {
            errorMessage.value = response._data.detail;
          },
        });

      } catch (error) {
        console.error('Error creating activity:', error);
      }
    };

    const fetch = async () => {
      try {
        const response = await $api(`/api/activities/`, {
          server: false,
          method: 'GET',

          onResponseError: ({ request, response, options }) => {
            console.error('Error fetching activities:', response);
          }
        });

        activities.value = response as ActivityType[];
        console.log('Activities fetched:', response);
      } catch (error) {
        console.error('Error fetching activities:', error);
      }
    };

    return { addNew, fetch };
  }
}
</script>

<style></style>