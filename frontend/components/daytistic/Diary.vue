<template>
    <div v-if="daytistic">
        <div class="flex items-center mb-6">
            <h2
                id="diary-entry-title"
                class="text-2xl font-semibold text-gray-900 mr-4"
            >
                Diary Entry
            </h2>
            <button
                @click="toggleDiaryEdit"
                class="text-indigo-600 hover:text-indigo-800 flex items-center transition duration-150 ease-in-out"
                :aria-label="isEditingDiary ? 'Cancel editing' : 'Edit diary entry'"
            >
                <component
                    :is="isEditingDiary ? X : Edit2"
                    class="w-5 h-5 mr-1"
                />
                <span class="text-sm font-medium">{{ isEditingDiary ? 'Cancel' : 'Edit' }}</span>
            </button>
        </div>
        <div class="bg-gray-50 p-6 rounded-lg shadow-sm">
            <div
                v-if="!isEditingDiary"
                class="prose max-w-none"
            >
                <p class="text-gray-700">
                    {{ props.daytistic.diary.entry }}
                </p>
                <div class="mt-6">
                    <h3 class="text-lg font-medium text-gray-900 mb-3">Moment of Happiness</h3>
                    <p class="text-gray-700">
                        {{ props.daytistic.diary.moment_of_happiness }}
                    </p>
                </div>
            </div>
            <div v-else>
                <label
                    for="diary-entry"
                    class="block text-sm font-medium text-gray-700 mb-2"
                    >Diary Entry</label
                >
                <textarea
                    id="diary-entry"
                    v-model="editedDiaryEntry"
                    class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                    rows="4"
                ></textarea>
                <label
                    for="moment-of-happiness"
                    class="block text-sm font-medium text-gray-700 mb-2"
                    >Moment of Happiness</label
                >
                <textarea
                    id="moment-of-happiness"
                    v-model="editedMomentOfHappiness"
                    class="w-full p-3 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-4"
                    rows="2"
                ></textarea>
                <button
                    @click=""
                    class="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    Save Changes
                </button>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Edit2, X } from 'lucide-vue-next';
import type { Daytistic } from '~/types/daytistics';

const props = defineProps<{
    daytistic: Daytistic;
}>();

const { isEditingDiary, editedDiaryEntry, editedMomentOfHappiness } = useForm();

const toggleDiaryEdit = () => {
    if (isEditingDiary.value) {
        editedDiaryEntry.value = props.daytistic.diary.entry;
        editedMomentOfHappiness.value = props.daytistic.diary.moment_of_happiness;
    }
    isEditingDiary.value = !isEditingDiary.value;
};

function useForm() {
    const isEditingDiary = ref(false);
    const editedDiaryEntry = ref('');
    const editedMomentOfHappiness = ref('');

    watch(
        () => props.daytistic,
        (newDaytistic) => {
            if (newDaytistic && newDaytistic.diary) {
                editedDiaryEntry.value = newDaytistic.diary.entry;
                editedMomentOfHappiness.value = newDaytistic.diary.moment_of_happiness;
            }
        },
        { immediate: true }
    );

    return {
        isEditingDiary,
        editedDiaryEntry,
        editedMomentOfHappiness,
    };
}
</script>
