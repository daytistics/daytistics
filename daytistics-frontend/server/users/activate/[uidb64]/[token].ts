import { useRouter } from 'nuxt/app';

export default defineEventHandler(async (event) => {
    // Get query params
    const uidb64 = event.context.params.uidb64;
    const token = event.context.params.token;

    const response = await $fetch(`/api/users/activate/${uidb64}/${token}`);

    if (response && response.success) {
        // Redirect to login page
        useRouter().push('/login');
    } else {
        // Redirect to error page
        useRouter().push('/error');
    }
});
