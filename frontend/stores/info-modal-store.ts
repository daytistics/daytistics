import { defineStore } from 'pinia';

export const useInfoDialogStore = defineStore({
    id: 'infoDialogStore',
    state: () => ({
        content: null as HTMLElement | null | string,
        heading: '',
        open: false,
    }),
    actions: {
        showInfoDialog(options: {
            content: HTMLElement | string;
            heading: string;
        }) {
            this.content = options.content;
            this.heading = options.heading;
            this.open = true;
        },
        hideInfoDialog() {
            this.content = null;
            this.heading = '';
            this.open = false;
        },
    },
});
