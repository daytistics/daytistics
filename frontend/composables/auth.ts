import { jwtDecode } from 'jwt-decode';

export const useAuth = () => {
    const { $api } = useNuxtApp();

    async function verifyAuth() {
        const accessTokenCookie = useCookie('access_token');
        let verified = false;

        if (!accessTokenCookie || typeof accessTokenCookie.value !== 'string') {
            return false;
        }

        try {
            await $api('/api/token/verify', {
                method: 'POST',
                body: {
                    token: accessTokenCookie.value,
                },

                onResponseError: ({ response }) => {
                    if (response.status === 401) {
                        verified = false;
                    }
                },

                onResponse: ({ response }) => {
                    if (response.status === 200) {
                        verified = true;
                    }
                },
            });
        } catch (error) {
            verified = false;
        }

        return verified;
    }

    async function renewAuth() {
        const refreshTokenCookie = useCookie('refresh_token');

        try {
            await $api('/api/token/refresh', {
                method: 'POST',
                body: JSON.stringify({ refresh: refreshTokenCookie.value }),

                onResponse: ({ response }) => {
                    if (response.status === 200) {
                        const { access, refresh } = response._data;
                        useCookie('access_token').value = access;
                        refreshTokenCookie.value = refresh;
                    }
                },
            });
        } catch (error) {
            return false;
        }

        return true;
    }

    function removeAuth() {
        useCookie('access_token').value = null;
        useCookie('refresh_token').value = null;

        useRouter().push('/');
    }

    function isTokenExpired(token: string): boolean {
        try {
            const decoded = jwtDecode(token);
            return (decoded.exp as number) < Date.now() / 1000;
        } catch (error) {
            return true;
        }
    }

    return {
        verifyAuth,
        renewAuth,
        removeAuth,
        isTokenExpired,
    };
};
