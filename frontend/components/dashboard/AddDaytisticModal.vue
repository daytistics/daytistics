<template>
  <div id="add-daytistic-modal" tabindex="-1" aria-hidden="true"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Add New Daytistic
          </h3>
          <button type="button" @click="closeModal"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>

        <!-- Modal body -->
        <form @submit.prevent="form.submit" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label for="type" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">What day are we
                talking about here?</label>
              <div class="relative max-w-sm">
                <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                  <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z" />
                  </svg>
                </div>
                <ThirdpartyDatepicker />
              </div>
            </div>
          </div>
          <p id="error" class="text-red-500 mb-3">
            {{ errorMessage }}
          </p>
          <button type="submit" class="inline-flex button bg-secondary hover:bg-secondary-dark items-center">
            <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd"
                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                clip-rule="evenodd"></path>
            </svg>
            <span>Add</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { initModals, Modal } from 'flowbite';

const emits = defineEmits(['close']);

const { errorMessage, create: createDaytistic } = useDaytisticsCreationAPI();
const form = useForm();
const { closeModal } = useModal();

onMounted(() => {
  initModals();
});

function useForm() {
  const date = useState<Date | null>('datepickerValue');

  const submit = async () => {

    if (!date.value) {
      errorMessage.value = 'Please select a date';
      return;
    }

    await createDaytistic((date.value as Date).toISOString().split('T')[0]);
  };

  return { date, submit };
}

function useDaytisticsCreationAPI() {
  const { $api } = useNuxtApp();
  const errorMessage = ref<string>('');

  const create = async (dateString: string) => {
    await $api('/api/daytistics/create', {
      server: false,
      method: 'POST',
      body: {
        date: dateString,
      },

      onResponse: ({ request, response, options }) => {
        if (response.status === 201) {
          console.log('Success');
          useRouter().push(
            `/dashboard/daytistics/${response._data.id}`
          );
        }
      },
      onResponseError: ({ request, response, options }) => {
        errorMessage.value = response._data.detail;
      },
    });
  };

  return { create, errorMessage };
}
function useModal() {
  const modal = ref<Modal | null>(null);

  const closeModal = () => {
    if (modal.value) {
      modal.value.hide();
      emits('close');
    }
  };

  onMounted(() => {
    modal.value = new Modal(document.getElementById('add-daytistic-modal'));
  });

  return { modal, closeModal };
}

</script>
