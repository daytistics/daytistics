export async function obtainToken(): Promise<string> {
    if (sessionStorage.getItem('csrf_token') !== null) {
        return sessionStorage.getItem('csrf_token') as string;
    }

    await useFetch('/api/csrf', {
        server: false,
        method: 'GET',

        onResponse: ({ response }) => {
            sessionStorage.setItem('csrf_token', response._data.csrf_token);
        },
    }).catch((error) => {
        console.error('Error generating CSRF token:', error);
    });

    return sessionStorage.getItem('csrf_token') as string;
}
