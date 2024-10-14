import { Modal } from 'flowbite';
import { defineStore } from 'pinia';

export const useErrorModalStore = defineStore({
    id: 'errorModalStore',
    state: () => ({
        message: '',
        docsLink: '',
        error: '',
        open: false,
    }),
    actions: {
        showErrorModal(options: {
            message: string;
            error?: string | null;
            docsLink?: string | null;
        }) {
            this.message = options.message;
            this.docsLink = options.docsLink || '';
            this.error = options.error || '';
            new Modal(document.getElementById('error-modal')).show();
            this.open = true;
        },
        closeErrorModal() {
            this.message = '';
            this.docsLink = '';
            this.error = '';
            new Modal(document.getElementById('error-modal')).hide();
            this.open = false;
        },
    },
});
