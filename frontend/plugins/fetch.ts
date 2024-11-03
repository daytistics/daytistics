export default defineNuxtPlugin((nuxtApp) => {
    const authStore = useAuthStore();

    const api = $fetch.create({
        async onResponseError({ response }) {
            if (response.status === 401) {
                await nuxtApp.runWithContext(() => navigateTo('/login'));
            }
        },
        async onRequest({ options }) {
            if (authStore.isAuthExpired()) {
                await authStore.refreshAuth();
            }

            options.headers.set(
                'Authorization',
                `Bearer ${useCookie('access_token').value as string}`
            );

            if (options.method === 'POST' || options.method === 'PUT') {
                options.headers.set('Content-Type', 'application/json');
                options.headers.set('X-CSRFToken', await authStore.getCsrfToken());
            }
        },
    });

    return {
        provide: {
            api,
        },
    };
});
