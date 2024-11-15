<template>
    <CommonDialog
        title="Add Daytistic"
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
                        >What day are we talking about here?</label
                    >
                    <div class="relative max-w-sm">
                        <div
                            class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none w-fit"
                        >
                            <svg
                                class="w-4 h-4 text-gray-500 dark:text-gray-400"
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
                        <CommonDatepicker
                            @update="form.handleDateUpdate"
                            class="w-fit"
                        />
                    </div>
                </div>
            </div>
            <p
                id="error"
                class="text-red-500 mb-3"
            >
                {{ errorMessage }}
            </p>
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
    </CommonDialog>
</template>

<script lang="ts" setup>
const emit = defineEmits(['close']);

const props = defineProps<{
    open: boolean;
}>();

const { errorMessage, create: createDaytistic } = useDaytisticsCreationAPI();
const form = useForm();

const isOpen = ref(false);

function closeDialog() {
    emit('close');
}

onUpdated(() => {
    isOpen.value = props.open;
});

function useForm() {
    const date = ref<Date | null>(null);

    const submit = async () => {
        if (!date.value) {
            errorMessage.value = 'Please select a date';
            return;
        }

        await createDaytistic((date.value as Date).toISOString().split('T')[0]);
    };

    const handleDateUpdate = (newDate: Date) => {
        date.value = newDate;
    };

    return { date, submit, handleDateUpdate };
}

function useDaytisticsCreationAPI() {
    const errorMessage = ref<string>('');

    const { $api } = useNuxtApp();

    const create = async (dateString: string) => {
        await $api('/api/daytistics/create', {
            method: 'POST',
            body: {
                date: dateString,
            },

            onResponse: ({ request, response, options }) => {
                if (response.status === 201) {
                    console.log('Success');
                    useRouter().push(`/app/daytistics/${response._data.id}`);
                }
            },
            onResponseError: ({ request, response, options }) => {
                errorMessage.value = response._data.detail;
            },
        });
    };

    return { create, errorMessage };
}
</script>
