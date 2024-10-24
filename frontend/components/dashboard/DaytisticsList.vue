<template>
    <DashboardAddDaytisticDialog
        :open="isAddingDaytistic"
        @close="isAddingDaytistic = false"
    />

    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex flex-row gap-3">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
                Your Daytistics
            </h3>
            <button
                @click="isAddingDaytistic = true"
                class="text-secondary hover:text-secondary-dark flex items-center transition duration-150 ease-in-out"
            >
                <Plus class="w-5 h-5 mr-1" />
                <span class="text-sm font-medium">Add New</span>
            </button>
        </div>
        <div class="border-t border-gray-200">
            <div class="px-4 py-5 sm:p-6">
                <div class="flex items-center justify-between mb-4">
                    <input
                        type="text"
                        placeholder="Search date..."
                        class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    />
                    <button
                        class="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-secondary hover:bg-secondary-dark"
                    >
                        Search
                    </button>
                </div>
                <ul class="divide-y divide-gray-200">
                    <li
                        v-for="(daytistic, index) in daytistics"
                        :key="index"
                        class="py-4 cursor-pointer hover:bg-gray-50"
                    >
                        <NuxtLink :to="`/daytistics/${daytistic.id}`">
                            <div class="flex items-center space-x-4">
                                <Calendar class="h-6 w-6 text-gray-400" />
                                <div class="flex-1 min-w-0">
                                    <p
                                        class="text-sm font-medium text-gray-900 truncate"
                                    >
                                        {{
                                            new Date(
                                                daytistic.date
                                            ).toLocaleDateString()
                                        }}
                                    </p>
                                    <p class="text-sm text-gray-500 truncate">
                                        {{ daytistic.total_activities }}
                                        Activities /
                                        {{ daytistic.total_duration }}
                                    </p>
                                </div>
                            </div>
                        </NuxtLink>
                    </li>
                    <div class="flex justify-center">
                        <span
                            v-show="totalPages === 0"
                            class="text-lg"
                        >
                            We couldn't find any daytistics for you. Why not
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
                <div class="mt-4 flex items-center justify-between">
                    <button
                        :disabled="currentPage === 1"
                        @click="currentPage--"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        Previous
                    </button>
                    <span
                        v-show="totalPages > 0"
                        class="text-sm text-gray-700"
                    >
                        Page {{ currentPage }} of {{ totalPages }}
                    </span>
                    <button
                        :disabled="currentPage === totalPages"
                        @click="currentPage++"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Calendar, Plus } from 'lucide-vue-next';
import type { Daytistic } from '~/types/daytistics';
const daytistics = ref<Daytistic[] | []>([]);

const listDaytisticsAPI = useListDaytisticsAPI();

const currentPage = ref(1);
const totalPages = ref(1);
const isAddingDaytistic = ref(false);

watch(currentPage, async (newPage) => {
    if (totalPages.value > 0) {
        await listDaytisticsAPI.loadPage(newPage);
    }
});

onMounted(async () => {
    await listDaytisticsAPI.loadPage(currentPage.value);
});

function useListDaytisticsAPI() {
    const { $api } = useNuxtApp();

    const list = async (page: number) => {
        return $api(`/api/daytistics/list?page=${page}`, {
            server: false,
            method: 'GET',
        });
    };

    const loadPage = async (page: number) => {
        const response: any = await list(page);
        daytistics.value = response.items;
        totalPages.value = Math.ceil(response.count / 5);
    };
    return {
        loadPage,
    };
}
</script>
