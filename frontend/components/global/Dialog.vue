<template>
    <Dialog
        :open="open"
        class="relative z-50"
        :aria-label="description"
    >
        <div
            class="fixed inset-0 bg-gray-900 opacity-50 z-40"
            aria-hidden="true"
        ></div>

        <div class="fixed inset-0 flex w-screen items-center justify-center p-4 z-50">
            <DialogPanel
                class="w-full shadow-md rounded-xl bg-white p-5"
                :class="props.maxWidth || 'max-w-lg'"
            >
                <div class="flex flex-row justify-between items-center">
                    <DialogTitle class="font-semibold text-xl">{{ title }}</DialogTitle>

                    <button
                        aria-label="Close dialog"
                        type="button"
                        @click="closeDialog"
                    >
                        <X />
                    </button>
                </div>
                <div class="mt-3">
                    <slot />
                </div>
            </DialogPanel>
        </div>
    </Dialog>
</template>

<script lang="ts" setup>
import { Dialog, DialogTitle, DialogPanel } from '@headlessui/vue';
import { X } from 'lucide-vue-next';

const emits = defineEmits(['close']);

const props = defineProps<{
    title: string;
    open: boolean;
    description?: string;
    maxWidth?: string;
}>();

onMounted(() => {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeDialog();
        }
    });

    if (import.meta.dev && !props.description) {
        console.warn(
            "Please provide a description prop to the Dialog component. This description will be used as the dialog's aria-label. Aria-labels are mandatory from the end of June 2025."
        );
    }
});

onUnmounted(() => {
    document.removeEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeDialog();
        }
    });

    closeDialog();
});

function closeDialog() {
    emits('close');
}
</script>
