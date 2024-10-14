// FIXME; Why the fuck says the server sometimes that the access token is invalid, even though it was renewed 2ms before?????

export default defineNuxtPlugin((nuxtApp) => {
    const api = $fetch.create({
        baseURL: process.env.BACKEND_URL,
        async onRequest({ request, options, error }) {
            const accessTokenCookie = useCookie('access_token');
            const { renewAuth, isTokenExpired } = useAuth();

            if (useRoute().path.includes('dashboard')) {
                if (isTokenExpired(accessTokenCookie.value as string)) {
                    if (!(await renewAuth())) {
                        await nuxtApp.runWithContext(() =>
                            navigateTo('/auth/login')
                        );
                        return;
                    }
                }
            }

            const csrfToken = await obtainToken();

            console.log('CSRF token:', csrfToken);

            // Add the access token to the request
            const headers = (options.headers ||= {});
            if (Array.isArray(headers)) {
                headers.push([
                    'Authorization',
                    `Bearer ${accessTokenCookie.value}`,
                ]);
                headers.push(['X-CSRFToken', csrfToken as string]);
            } else if (headers instanceof Headers) {
                headers.set(
                    'Authorization',
                    `Bearer ${accessTokenCookie.value}`
                );
                headers.set('X-CSRFToken', csrfToken as string);
            } else {
                headers.Authorization = `Bearer ${accessTokenCookie.value}`;
                headers['X-CSRFToken'] = csrfToken as string;
            }
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
