<template>
    <!-- Dialog to create a new Daytistic - the span is used for testing purposes -->
    <span
        aria-hidden="true"
        :data-dialog-open-test="isAddingDaytistic"
    ></span>
    <Dialog
        title="Add Daytistic"
        :open="isAddingDaytistic"
        size="md"
        @close="isAddingDaytistic = false"
    >
        <DashboardCreateDaytisticContent @submit="isAddingDaytistic = false" />
    </Dialog>

    <!-- Actual list -->

    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex flex-row gap-3 justify-between items-center">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Your Daytistics</h3>
            <button
                @click="isAddingDaytistic = true"
                class="text-secondary hover:text-tertiary flex items-center transition duration-150 ease-in-out"
            >
                <Plus class="w-6 md:w-5 h-auto md:mr-1" />
                <span class="text-sm font-medium hidden md:block">Add New</span>
            </button>
        </div>
        <div class="border-t border-gray-200">
            <div
                class="flex justify-center my-20"
                v-if="isFetching"
            >
                <Loader />
            </div>
            <div
                v-else
                class="px-4 py-5 sm:p-6"
            >
                <ul class="divide-y divide-day-gray-medium">
                    <li
                        v-for="(daytistic, index) in daytistics"
                        :key="index"
                        class="py-4 cursor-pointer hover:bg-day-gray-light"
                    >
                        <NuxtLink :to="`/dashboard/daytistics/${daytistic.id}`">
                            <div class="flex items-center space-x-4 px-3">
                                <Calendar class="h-6 w-6 text-day-gray-dark" />
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-dark truncate">
                                        {{ new Date(daytistic.date).toLocaleDateString() }}
                                    </p>
                                    <p class="text-sm text-day-gray-dark truncate">
                                        {{ daytistic.total_activities }}
                                        Activities /
                                        {{ readableTotalDuration(daytistic.total_duration) }}
                                    </p>
                                </div>
                            </div>
                        </NuxtLink>
                    </li>
                    <div class="flex justify-center">
                        <span
                            v-show="totalPages === 0"
                            class="text-md text-center"
                        >
                            We couldn't find any Daytistics for you. Why not
                            <button
                                type="button"
                                class="text-secondary"
                            >
                                create
                            </button>
                            one?
                        </span>
                    </div>
                </ul>
                <div
                    v-if="totalPages > 0"
                    class="mt-4 flex items-center justify-between"
                >
                    <button
                        :disabled="currentPage === 1"
                        @click="decreasePage"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        <span class="hidden md:block">Previous</span>
                        <ChevronLeft class="md:hidden" />
                    </button>
                    <span class="text-sm text-gray-700">
                        <span class="hidden md:inline-block">Page</span>
                        {{ currentPage }} of {{ totalPages }}
                    </span>
                    <button
                        :disabled="currentPage === totalPages"
                        @click="increasePage"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        <span class="hidden md:block">Next</span>
                        <ChevronRight class="md:hidden" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Calendar, Plus, ChevronLeft, ChevronRight } from 'lucide-vue-next';
import useEndpoints from '~/composables/useEndpoints';
import type { Daytistic } from '~/types/daytistics';

const daytistics = ref<Daytistic[] | []>([]);
const currentPage = ref(1);
const totalPages = ref(1);
const isFetching = ref(false);
const isAddingDaytistic = ref(false);
const { listDaytistics } = useEndpoints();

async function increasePage() {
    currentPage.value++;
    await loadPage(currentPage.value);
}

async function decreasePage() {
    if (currentPage.value === 0) {
        return;
    }

    currentPage.value--;
    await loadPage(currentPage.value);
}

const loadPage = async (page: number) => {
    isFetching.value = true;
    const response = await listDaytistics(page);
    daytistics.value = response.items;
    totalPages.value = Math.ceil(response.count / 5);
    isFetching.value = false;
};

const readableTotalDuration = (duration: number) => {
    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;
    return `${hours}h ${minutes}m`;
};

onMounted(async () => {
    await loadPage(currentPage.value);
});
</script>
