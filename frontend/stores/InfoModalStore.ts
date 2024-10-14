import { Modal } from 'flowbite';
import { defineStore } from 'pinia';

export const useInfoModalStore = defineStore({
    id: 'infoModalStore',
    state: () => ({
        content: null as HTMLElement | null | string,
        heading: '',
        open: false,
    }),
    actions: {
        showInfoModal(options: {
            content: HTMLElement | string;
            heading: string;
        }) {
            this.content = options.content;
            this.heading = options.heading;
            new Modal(document.getElementById('info-modal')).show();
            this.open = true;
        },
        closeInfoModal() {
            this.content = null;
            this.heading = '';
            new Modal(document.getElementById('info-modal')).hide();
            this.open = false;
        },
    },
});
