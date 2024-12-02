<template>
    <VueDatePicker
        v-model="date"
        auto-apply
        :max-date="new Date()"
        :enable-time-picker="false"
        :format="date?.toLocaleDateString()"
        @update:model-value="handleUpdate"
    />
</template>

<script lang="ts" setup>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import '~/assets/css/vue-datepicker.css';

const date = ref<Date | null>(null);

const emit = defineEmits(['update']);

function handleUpdate(newDate: Date) {
    date.value = newDate;
    emit('update', newDate);
}
</script>
