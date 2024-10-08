export default defineNuxtRouteMiddleware(async (to, from) => {
    const { renewAuth } = useAuth();

    console.log('Global middleware');

    if (to.path.includes('dashboard')) {
        if (!(await renewAuth())) {
            return navigateTo('/auth/login');
        }
    }
});
