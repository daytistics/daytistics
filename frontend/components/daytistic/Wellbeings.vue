<template>
    <div v-if="daytistic">
        <h2
            id="wellbeing-ratings-title"
            class="text-2xl font-semibold text-gray-900 mb-6"
        >
            Well-being Ratings
        </h2>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div
                v-for="wellbeing in daytistic.wellbeing"
                :key="wellbeing.id"
                class="bg-gray-50 p-4 rounded-lg shadow-sm"
            >
                <h3 class="text-sm font-medium text-gray-500 mb-2">
                    {{ wellbeing.name }}
                </h3>
                <div class="flex items-center">
                    <div class="flex">
                        <Star
                            v-for="star in 5"
                            :key="star"
                            @click=""
                            class="text-yellow-400"
                        />
                    </div>
                    <span class="ml-2 text-sm text-gray-700"
                        >{{ wellbeing.rating }}/5</span
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Star } from 'lucide-vue-next';
import type { Daytistic } from '~/types/daytistics';

const props = defineProps<{
    daytistic: Daytistic;
}>();
</script>
