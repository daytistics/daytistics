<template>
    <CommonDialog
        :title="heading"
        :open="open"
        max-width="max-w-md"
        @close="hideInfoDialog()"
    >
        <div v-html="content"></div>
        <button
            @click="hideInfoDialog"
            type="button"
            class="button mt-4"
        >
            Okay 👍
        </button>
    </CommonDialog>
</template>

<script lang="ts" setup>
const infoDialogStore = useInfoDialogStore();
const { hideInfoDialog } = infoDialogStore;
const { content, heading, open } = storeToRefs(infoDialogStore);
</script>
