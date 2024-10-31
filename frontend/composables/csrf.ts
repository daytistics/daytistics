export const useCsrf = () => {
    const { $api } = useNuxtApp();
    const { backendUrl } = useRuntimeConfig().public;

    const obtainToken = async () => {
        debugger;
        if (
            useCookie('csrf_token').value &&
            typeof useCookie('csrf_token').value === 'string'
        ) {
            return useCookie('csrf_token').value as string;
        }

        await useFetch('/api/csrf', {
            method: 'GET',
            server: false,
            baseURL: backendUrl,
            onResponse: ({ response }) => {
                useCookie('csrf_token').value = response._data.csrf_token;
            },
        }).catch((error) => {
            console.error('Error generating CSRF token:', error);
        });

        return useCookie('csrf_token').value as string;
    };

    return {
        obtainToken,
    };
};
