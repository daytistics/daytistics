export default defineNuxtRouteMiddleware(async () => {
    const { isAuthExpired, refreshAuth } = useAuthStore();

    if (isAuthExpired()) {
        try {
            await refreshAuth();
        } catch {
            return navigateTo('/login');
        }
    }
});
