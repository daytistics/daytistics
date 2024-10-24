import { Modal } from 'flowbite';
import { defineStore } from 'pinia';

export const useErrorDialogStore = defineStore({
    id: 'errorDialogStore',
    state: () => ({
        message: '',
        docsLink: '',
        open: false,
    }),
    actions: {
        showErrorDialog(options: {
            message: string;
            docsLink?: string | null;
        }) {
            this.message = options.message;
            this.docsLink = options.docsLink || '';
            this.open = true;
        },
        hideErrorDialog() {
            this.message = '';
            this.docsLink = '';
            this.open = false;
        },
    },
});
