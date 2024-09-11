export function useCsrfToken() {
    const csrfToken = ref('');

    const generateToken = async () => {
        await $fetch('/api/de/csrf-token/', {
            server: false,
            method: 'GET',

            onResponse({ request, response, options }) {
                if (response.ok && response._data.csrfToken) {
                    csrfToken.value = response._data.csrfToken;

                    const csrfCookie = useCookie('csrf-token');
                    csrfCookie.value = csrfToken.value;
                } else {
                    console.error('Failed to generate CSRF token:', response);
                }
            },
        }).catch((error) => {
            console.error('Error generating CSRF token:', error);
        });
    };

    const getToken = () => {
        if (!csrfToken.value) {
            // Versuchen, den Token aus dem Cookie zu laden
            const csrfCookie = useCookie('csrf-token');
            csrfToken.value = csrfCookie.value || '';

            // Wenn kein Token im Cookie, generieren Sie einen neuen
            if (!csrfToken.value) {
                generateToken();
            }
        }
        return csrfToken.value;
    };

    return {
        getToken,
        generateToken,
    };
}
