<template>
    <form @submit.prevent="form.submit">
        <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
                <label
                    for="type"
                    class="block mb-2 text-sm font-medium text-dark"
                    >What day are we talking about here?</label
                >
                <div class="relative max-w-sm">
                    <div
                        class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none w-fit"
                    >
                        <svg
                            class="w-4 h-4 text-day-gray-dark"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                        >
                            <path
                                d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"
                            />
                        </svg>
                    </div>
                    <DatePicker
                        @update="form.handleDateUpdate"
                        class="w-fit"
                    />
                </div>
            </div>
        </div>
        <button
            type="submit"
            class="button"
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
            <span>Add</span>
        </button>
    </form>
</template>

<script lang="ts" setup>
import { useToast } from 'vue-toastification';
import useEndpoints from '~/composables/useEndpoints';

const emit = defineEmits(['close']);
const form = useForm();

function useForm() {
    const toast = useToast();
    const date = ref<Date | null>(null);

    const submit = async () => {
        if (!date.value) {
            toast.error('Please select a date');
            return;
        }

        try {
            const daytisticId = (await useEndpoints().createDaytistic(
                date.value as Date
            )) as number;
            await navigateTo(`/dashboard/daytistics/${daytisticId}`);
            toast.success('Daytistic created successfully');
        } catch (error) {
            toast.error('Failed to create daytistic');
        }
    };

    const handleDateUpdate = (newDate: Date) => {
        date.value = newDate;
    };

    return { date, submit, handleDateUpdate };
}
</script>
