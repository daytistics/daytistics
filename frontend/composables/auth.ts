import { jwtDecode } from 'jwt-decode';

export const useAuth = () => {
    async function verifyAuth() {
        const accessTokenCookie = useCookie('access_token');
        let verified = false;

        if (!accessTokenCookie || typeof accessTokenCookie.value !== 'string') {
            return false;
        }

        try {
            await useFetch('/api/token/verify', {
                server: true,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': await obtainToken(),
                },
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

        if (
            !refreshTokenCookie ||
            typeof refreshTokenCookie.value !== 'string'
        ) {
            return false;
        }

        try {
            const response = await useFetch('/api/token/refresh', {
                server: true,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': await obtainToken(),
                },
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
