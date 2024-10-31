export async function obtainToken(): Promise<string> {
    debugger;
    if (useCookie('csrf_token').value) {
        return useCookie('csrf_token').value as string;
    }

    await useFetch('/api/csrf', {
        method: 'GET',

        onResponse: ({ response }) => {
            useCookie('csrf_token').value = response._data.csrf_token;
        },
    }).catch((error) => {
        console.error('Error generating CSRF token:', error);
    });

    return useCookie('csrf_token').value as string;
}
