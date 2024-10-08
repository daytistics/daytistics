export const useAuth = () => {
    async function verifyAuth() {
        const accessTokenCookie = useCookie('access_token');

        if (!accessTokenCookie || typeof accessTokenCookie.value !== 'string') {
            return false;
        }

        try {
            const response = await useFetch('/api/token/verify', {
                server: true,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': useCsrf().getToken(),
                },
                body: {
                    token: accessTokenCookie.value,
                },
            });
        } catch (error) {
            console.error('Failed to verify access token', error);
            return false;
        }

        return true;
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
                    'X-CSRFToken': useCsrf().getToken(),
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
            console.error('Failed to renew access token', error);
            return false;
        }

        return true;
    }

    function removeAuth() {
        useCookie('access_token').value = null;
        useCookie('refresh_token').value = null;

        useRouter().push('/');
    }

    return {
        verifyAuth,
        renewAuth,
        removeAuth,
    };
};
