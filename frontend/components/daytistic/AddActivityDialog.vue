<template>
    <CommonDialog
        title="Add Activity"
        :open="isOpen"
        max-width="max-w-md"
        @close="
            isOpen = false;
            closeDialog();
        "
    >
        <form @submit.prevent="form.submit">
            <div class="grid gap-4 mb-4 grid-cols-2">
                <div class="col-span-2">
                    <label
                        for="type"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >What activity did you do that day?</label
                    >
                    <select
                        id="activity-type"
                        v-model="form.activityType"
                        required
                        class="input"
                    >
                        <option
                            v-for="activity in activities"
                            :key="activity.id"
                            :value="activity.id"
                        >
                            {{ activity.name }}
                        </option>
                    </select>
                </div>
                <div>
                    <label
                        for="start-time"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Start time:</label
                    >
                    <div class="relative">
                        <CommonTimepicker @update="form.handleStartTimeUpdate" />
                    </div>
                </div>
                <div>
                    <label
                        for="end-time"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >End time:</label
                    >
                    <div class="relative">
                        <CommonTimepicker @update="form.handleEndTimeUpdate" />
                    </div>
                </div>
            </div>
            <p
                id="activity-error"
                class="text-red-500 text-sm mb-4"
            >
                {{ form.errorMessage }}
            </p>
            <div class="flex justify-end md:justify-start">
                <button
                    type="submit"
                    class="inline-flex button bg-secondary hover:bg-secondary-dark items-center"
                >
                    <svg
                        class="me-1 -ms-1 w-5 h-5"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                            clip-rule="evenodd"
                        ></path>
                    </svg>
                    Add activity
                </button>
            </div>
        </form>
    </CommonDialog>
</template>

<script lang="ts" setup>
import { initModals, Modal } from 'flowbite';
import type { ActivityType } from '~/types/activities';

const emit = defineEmits(['submit', 'close']);

const props = defineProps<{
    open: boolean;
}>();

const form = useForm();
const { activities } = useActivitiesAPI();

const isOpen = ref(false);

onUpdated(() => {
    isOpen.value = props.open;
});

function closeDialog() {
    emit('close');
}

function useForm() {
    const { add } = useActivitiesAPI();

    const activityType = ref<number>(0);
    const startTime = ref<DateObject | null>(null);
    const endTime = ref<DateObject | null>(null);
    const errorMessage = ref<string>('');

    interface DateObject {
        hours: number;
        minutes: number;
    }

    const submit = async () => {
        const formattedStartTime = startTime.value
            ? startTime.value.hours * 60 + startTime.value.minutes
            : 0;
        const formattedEndTime = endTime.value
            ? endTime.value.hours * 60 + endTime.value.minutes
            : 0;
        await add(formattedStartTime, formattedEndTime);
    };

    const setError = (message: string) => {
        errorMessage.value = message;
    };

    const handleStartTimeUpdate = (newTime: DateObject) => {
        startTime.value = newTime;
    };

    const handleEndTimeUpdate = (newTime: DateObject) => {
        endTime.value = newTime;
    };

    return {
        submit,
        setError,
        activityType,
        startTime,
        endTime,
        errorMessage,
        handleStartTimeUpdate,
        handleEndTimeUpdate,
    };
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
        // CURRENT PROBLEM: CREATION NOT WORKING
        const id = useRoute().params.id;
        debugger;
        try {
            await $api(`/api/daytistics/${id}/add-activity`, {
                method: 'POST',
                body: {
                    id: form.activityType,
                    start_time: startTime,
                    end_time: endTime,
                },
                onResponse: ({ request, response, options }) => {
                    if (response.status === 201) {
                        emit('submit');
                        useModal().closeModal();
                        debugger;
                    }
                },
                onResponseError: ({ request, response, options }) => {
                    form.setError(response._data.detail);
                    debugger;
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
                },
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
