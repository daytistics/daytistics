export function useCsrf() {
    const csrfToken = ref('');

    const generateToken = async () => {
        await $fetch('/api/csrf/', {
            server: false,
            method: 'GET',
        }).catch((error) => {
            console.error('Error generating CSRF token:', error);
        });
    };

    const getToken = () => {
        if (!csrfToken.value) {
            // Versuchen, den Token aus dem Cookie zu laden
            const csrfCookie = useCookie('csrftoken');
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
