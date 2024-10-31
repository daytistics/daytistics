import type { UseFetchOptions } from 'nuxt/app';

const router = useRouter();
export function useCustomFetch<T>(
    url: string | (() => string),
    options: UseFetchOptions<T> = {}
) {
    return useFetch(url, {
        ...options,
        // @ts-ignore
        $fetch: useNuxtApp().$customFetch,
        async onRequest({ options }) {
            debugger;
            const accessTokenCookie = useCookie('access_token');
            const { renewAuth, isTokenExpired } = useAuth();
            const { obtainToken } = useCsrf();
            const headers = options.headers || new Headers();

            if (typeof useCookie('csrf_token').value !== 'string') {
                await obtainToken();
            }

            if (useCookie('refresh_token').value) {
                if (isTokenExpired(accessTokenCookie.value as string)) {
                    if (!(await renewAuth())) {
                        router.push('/login');
                        return;
                    }
                }
                headers.set(
                    'Authorization',
                    `Bearer ${accessTokenCookie.value}`
                );
            }
        },

        async onResponseError({ response, options }) {
            if (response.status == 401) {
                useCookie('access_token').value = null;
                useCookie('refresh_token').value = null;
                router.push('/login');
            }
        },
    });
}
