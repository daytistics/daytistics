<template>
    <div v-if="daytistic">
        <div class="flex items-center mb-6">
            <h2
                id="diary-entry-title"
                class="text-2xl font-semibold text-gray-900 mr-4"
            >
                Activities
            </h2>
            <button
                data-modal-target="add-activity-modal"
                data-modal-show="add-activity-modal"
                @click="openModal"
                class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out"
            >
                <Plus class="w-5 h-5 mr-1" />
                <span class="text-sm font-medium">Add New</span>
            </button>
        </div>
        <ul class="bg-gray-50 rounded-lg shadow-sm overflow-hidden">
            <li
                v-for="(activity, index) in daytistic?.activities"
                :key="activity.id"
                class="group"
            >
                <div
                    class="px-6 py-4 flex items-center justify-between hover:bg-gray-100 transition duration-150 ease-in-out cursor-pointer"
                    :class="{
                        'border-t border-gray-200': index !== 0,
                    }"
                >
                    <div>
                        <p
                            class="text-lg font-medium text-gray-900 group-hover:text-indigo-600 transition duration-150 ease-in-out"
                        >
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
                            class="w-5 h-5 text-gray-400 group-hover:text-indigo-600 transition duration-150 ease-in-out"
                        />
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<script lang="ts" setup>
import { initModals, Modal } from 'flowbite';
import { ChevronRight, Plus } from 'lucide-vue-next';
import type { Daytistic } from '~/types/daytistics';

const props = defineProps<{
    daytistic: Daytistic;
}>();

function formatTimeWindow(startTime: number, endTime: number): string {
    const startHours = Math.floor(startTime / 60);
    const startMinutes = startTime % 60;
    const endHours = Math.floor(endTime / 60);
    const endMinutes = endTime % 60;
    return `${startHours.toString().padStart(2, '0')}:${startMinutes.toString().padStart(2, '0')} - ${endHours
        .toString()
        .padStart(2, '0')}:${endMinutes.toString().padStart(2, '0')}`;
}

const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
};

function openModal() {
    const modalElement = document.getElementById(
        'add-activity-modal'
    ) as HTMLElement;
    const modal = new Modal(modalElement);
    modal.show();
}

onMounted(() => {
    initModals();
});
</script>
