<template>
    <CommonDialog
        title="An Error Occurred"
        :open="open"
        max-width="max-w-md"
        @close="hideErrorDialog()"
    >
        <p>
            {{ message }}
        </p>
        <div class="flex flex-row gap-3 mt-4">
            <button
                @click="hideErrorDialog"
                type="button"
                class="button"
            >
                Okay 😥
            </button>
            <div class="flex justify-center items-center">
                <NuxtLink
                    v-if="docsLink"
                    :to="docsLink"
                    class="text-secondary hover:text-secondary-dark"
                >
                    Learn More
                </NuxtLink>
            </div>
        </div>
    </CommonDialog>
</template>

<script lang="ts" setup>
const errorDialogStore = useErrorDialogStore();
const { hideErrorDialog } = errorDialogStore;
const { message, docsLink, open } = storeToRefs(errorDialogStore);
</script>
