type Callback = (...args: any[]) => void;

export async function requireAuth(
    callback: Callback,
    ...params: any[]
): Promise<boolean> {
    const auth = useAuth();

    if (!auth.isAuthenticated()) {
        return false;
    }

    const tokenRefreshedSuccessfully = await auth.refresh();

    if (!tokenRefreshedSuccessfully) {
        return false;
    }

    try {
        await callback(...params);
    } catch (error) {
        return false;
    }

    return true;
}

export const useAuth = () => {
    const isAuthenticated = async (): Promise<boolean> => {
        let isTokenValid = false;

        await useFetch('/api/token/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': useCsrf().getToken(),
            },
            body: JSON.stringify({ token: useCookie('access_token').value }),

            onResponse: async ({ request, response, options }) => {
                if (response.status === 200) {
                    isTokenValid = true;
                }
            },
        });

        return isTokenValid;
    };

    const refresh = async () => {
        const refreshTokenCookie = useCookie('refresh_token');

        let success = false;

        await $fetch('api/token/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': useCsrf().getToken(),
            },
            body: JSON.stringify({ refresh: refreshTokenCookie.value }),

            onResponse: ({ request, response, options }) => {
                if (response.status === 200) {
                    const data = response._data;

                    const accessTokenCookie = useCookie('access_token');
                    refreshTokenCookie.value = data.refresh;
                    accessTokenCookie.value = data.access;
                    success = true;
                } else {
                    success = false;
                }
            },
        });

        return success;
    };
    return {
        isAuthenticated,
        refresh,
    };
};
