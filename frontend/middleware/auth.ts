export default defineNuxtRouteMiddleware(async (to, from) => {
    const { isAuthExpired, refreshAuth } = useAuthStore();
    if (isAuthExpired()) {
        try {
            await refreshAuth();
        } catch (error) {
            return navigateTo('/login');
        }
    }
});
