<template>
  <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" :draggable="false" modal
    header="Create Daytistic">
    <div class="flex items-center gap-4 mb-8">
      <p class="font-semibold">Date</p>
      <DatePicker v-model="date" />
    </div>
    <div class="flex items-center gap-4 mb-8">
      <p class="font-semibold">Important</p>
      <Checkbox v-model="checked" :binary="true" />
    </div>
    <div class="flex justify-end gap-2">
      <Button type="button" label="Save" @click="handleClose"></Button>
    </div>

  </Dialog>
</template>

<script lang="ts" setup>

const emit = defineEmits(['close', 'update:visible']);

defineProps({
  visible: Boolean
});

const checked = ref(false);
const date = ref(new Date());

const handleClose = () => {
  emit('close');
}
</script>
