import { jwtDecode } from 'jwt-decode';

export const useUser = () => {
    const isAuthenticated = async () => {
        checkAndRenewToken();
        var isAuthenticated = false;

        await $fetch('/api/users/auth/', {
            server: false,
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': useCsrfToken().getToken(),
                Authorization: `Bearer ${useCookie('access_token').value}`,
            },
            onResponse: ({ request, response, options }) => {
                if (response.status === 200) {
                    isAuthenticated = true;
                } else {
                    isAuthenticated = false;
                }
            },
        }).catch((error) => {
            isAuthenticated = false;
        });

        return isAuthenticated;
    };

    const checkAndRenewToken = async () => {
        const accessTokenCookie = useCookie('access_token');

        if (!accessTokenCookie.value) {
            return;
        }

        const expirationTime = jwtDecode(accessTokenCookie.value).exp; // Entschlüssle das JWT, um das Ablaufdatum zu erhalten
        const currentTime = Math.floor(Date.now() / 1000);

        if (!expirationTime || !currentTime) {
            return;
        }

        // Erneuere das Token, wenn es bald abläuft (z.B. in weniger als 1 Minute)
        if (expirationTime - currentTime < 60) {
            const refreshTokenCookie = useCookie('refresh_token');

            if (!refreshTokenCookie.value) {
                return;
            }

            await $fetch('api/users/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshTokenCookie.value }),

                onResponse: ({ request, response, options }) => {
                    if (response.status === 200) {
                        const data = response._data;

                        refreshTokenCookie.value = data.refreshToken;
                        accessTokenCookie.value = data.accessToken;
                    }
                },
            });
        }
    };

    const getData = async () => {
        var data = {};
        checkAndRenewToken();

        await $fetch('/api/users/data/', {
            server: false,
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': useCsrfToken().getToken(),
                Authorization: `Bearer ${useCookie('access_token').value}`,
            },
            onResponse: ({ request, response, options }) => {
                if (response.status === 200) {
                    data = response._data;
                }
            },
        });

        return data;
    };

    return {
        isAuthenticated,
        getData,
    };
};
