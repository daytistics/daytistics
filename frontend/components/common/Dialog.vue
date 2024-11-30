<template>
    <ClientOnly>
        <Dialog
            :open="open"
            class="relative z-50"
        >
            <div
                class="fixed inset-0 bg-black/30"
                aria-hidden="true"
            />

            <div class="fixed inset-0 flex w-screen items-center justify-center p-4">
                <DialogPanel
                    class="w-full shadow-md rounded-xl bg-white p-5"
                    :class="props.maxWidth || 'max-w-lg'"
                >
                    <div class="flex flex-row justify-between items-center">
                        <DialogTitle class="font-semibold text-xl">{{ title }}</DialogTitle>

                        <button
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
    </ClientOnly>
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

function closeDialog() {
    emits('close');
}
</script>
