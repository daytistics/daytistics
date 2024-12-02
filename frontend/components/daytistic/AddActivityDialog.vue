<template>
    <Dialog
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
                        class="block mb-2 text-sm font-medium text-gray-900"
                        >What activity did you do that day?</label
                    >
                    <AutoCompleteInput :items="activities as unknown as string[]" />
                </div>
                <div>
                    <label
                        for="start-time"
                        class="block mb-2 text-sm font-medium text-gray-900"
                        >Start time:</label
                    >
                    <div class="relative">
                        <TimePicker @update="form.handleStartTimeUpdate" />
                    </div>
                </div>
                <div>
                    <label
                        for="end-time"
                        class="block mb-2 text-sm font-medium text-gray-900"
                        >End time:</label
                    >
                    <div class="relative">
                        <TimePicker @update="form.handleEndTimeUpdate" />
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
    </Dialog>
</template>

<script lang="ts" setup>
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

function useActivitiesAPI() {
    const activities = ref<ActivityType[]>([]);
    const { $api } = useNuxtApp();

    const add = async (startTime: number, endTime: number) => {
        // CURRENT PROBLEM: CREATION NOT WORKING
        const id = useRoute().params.id;

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
                },
            });
        } catch (error) {
            console.error('Error fetching activities:', error);
        }
    };

    onMounted(async () => {
        await fetch();
    });

    return { add, fetch, activities };
}
</script>

<style></style>
