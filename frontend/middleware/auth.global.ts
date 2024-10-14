export default defineNuxtRouteMiddleware(async (to, from) => {
    const { renewAuth, isTokenExpired } = useAuth();

    if (to.path.includes('dashboard')) {
        if (
            isTokenExpired(useCookie('access_token').value as string) &&
            !isTokenExpired(useCookie('refresh_token').value as string)
        ) {
            if (!(await renewAuth())) {
                await useNuxtApp().runWithContext(() =>
                    navigateTo('/auth/login')
                );
                return;
            }
        }
    }
});
