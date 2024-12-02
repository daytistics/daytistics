import Toast, { type PluginOptions, POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css';

export default defineNuxtPlugin((nuxtApp) => {
    const options: PluginOptions = {
        position: POSITION.BOTTOM_RIGHT,
    };

    nuxtApp.vueApp.use(Toast, options);
});
