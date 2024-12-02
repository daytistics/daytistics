<template>
    <VueDatePicker
        class="input"
        v-model="time"
        auto-apply
        :enable-time-picker="true"
        :time-picker="true"
        @update:model-value="handleUpdate"
    >
        <template #input-icon>
            <ClockIcon class="w-4 h-4 text-gray-400" />
        </template>
    </VueDatePicker>
</template>

<script lang="ts" setup>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { ClockIcon } from 'lucide-vue-next';
import '~/assets/css/vue-datepicker.css';

const time = ref<Date | null>(null);

const emit = defineEmits(['update']);

function handleUpdate(newTime: Date) {
    time.value = newTime;
    emit('update', newTime);
}
</script>
