import type { CookieRef } from '#app';

export default defineNuxtPlugin((nuxtApp) => {
    const api = $fetch.create({
        baseURL: process.env.BACKEND_URL,
        async onRequest({ request, options, error }) {
            const accessTokenCookie = useCookie('access_token');
            const { renewAuth } = useAuth();

            if (!(await renewAuth())) {
                await nuxtApp.runWithContext(() => navigateTo('/auth/login'));
                return;
            }

            // Add the access token to the request
            const headers = (options.headers ||= {});
            if (Array.isArray(headers)) {
                headers.push([
                    'Authorization',
                    `Bearer ${accessTokenCookie.value}`,
                ]);
                headers.push(['X-CSRFToken', useCsrf().getToken()]);
            } else if (headers instanceof Headers) {
                headers.set(
                    'Authorization',
                    `Bearer ${accessTokenCookie.value}`
                );
                headers.set('X-CSRFToken', useCsrf().getToken());
            } else {
                headers.Authorization = `Bearer ${accessTokenCookie.value}`;
                headers['X-CSRFToken'] = useCsrf().getToken();
            }

            console.log('[fetch request]', request);
        },

        async onResponseError({ response }) {
            if (response.status === 401) {
                await nuxtApp.runWithContext(() => navigateTo('/auth/login'));
            }
        },
    });

    // Expose to useNuxtApp().$api
    return {
        provide: {
            api,
        },
    };
});
