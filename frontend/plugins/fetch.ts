// FIXME; Why the fuck says the server sometimes that the access token is invalid, even though it was renewed 2ms before?????

export default defineNuxtPlugin((nuxtApp) => {
    const api = 0; // $fetch.create({
    //     baseURL: `${useRuntimeConfig().public.backendUrl}`,
    //     credentials: 'include',
    //     async onRequest({ options }) {
    //         const accessTokenCookie = useCookie('access_token');
    //         const { renewAuth, isTokenExpired } = useAuth();
    //         const { obtainToken } = useCsrf();

    //         if (!useCookie('csrf_token').value) {
    //             await obtainToken();
    //         }

    //         if (useCookie('refresh_token').value) {
    //             if (isTokenExpired(accessTokenCookie.value as string)) {
    //                 if (!(await renewAuth())) {
    //                     await nuxtApp.runWithContext(() =>
    //                         navigateTo('/login')
    //                     );
    //                     return;
    //                 }
    //             }
    //             headers.set(
    //                 'Authorization',
    //                 `Bearer ${accessTokenCookie.value}`
    //             );
    //         }
    //     },

    //     async onResponseError({ response, options }) {
    //         if (response.status == 401) {
    //             useCookie('access_token').value = null;
    //             useCookie('refresh_token').value = null;
    //             await nuxtApp.runWithContext(() => navigateTo('/login'));
    //         }
    //     },
    // });

    return {
        provide: {
            api,
        },
    };
});
