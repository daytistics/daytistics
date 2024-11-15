import { defineStore } from 'pinia';
import { AuthenticationStatus, type User } from '~/types/user-types';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore({
    id: 'authStore',
    state: () => ({
        user: null as User | null,
        status: AuthenticationStatus.UNAUTHENTICATED,
        csrfToken: null as string | null,
    }),
    actions: {
        /**
         * Logs the user in and stores the tokens in cookies. The authentication status is set to AUTHENTICATED
         * @param email
         * @param password
         * @throws {Error} If the login fails. This error is the error returned by the server
         */
        async login(email: string, password: string): Promise<void | never> {
            this.status = AuthenticationStatus.PENDING;
            console.log(await this.getCsrfToken());
            try {
                await $fetch('/api/users/login', {
                    method: 'POST',
                    body: {
                        email,
                        password,
                    },
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': await this.getCsrfToken(),
                    },
                    onResponse: ({ response }) => {
                        if (response.status === 200) {
                            const accessToken = response._data.accessToken;
                            const refreshToken = response._data.refreshToken;

                            const accessTokenCookie = useCookie('access_token');
                            const refreshTokenCookie = useCookie('refresh_token');

                            accessTokenCookie.value = accessToken;
                            refreshTokenCookie.value = refreshToken;

                            this.status = AuthenticationStatus.AUTHENTICATED;
                        }
                    },
                });
            } catch (error) {
                this.status = AuthenticationStatus.UNAUTHENTICATED;
                throw error;
            }
        },

        /**
         * Logs the user out by deleting the tokens from cookies. The authentication status is set to UNAUTHENTICATED
         */
        logout(): void {
            this.status = AuthenticationStatus.PENDING;
            useCookie('access_token').value = null;
            useCookie('refresh_token').value = null;
            this.status = AuthenticationStatus.UNAUTHENTICATED;
        },

        /**
         * Registers a new user and logs them in. The authentication status is set to AUTHENTICATED
         * @param email
         * @param password
         * @param username
         * @throws {Error} If the registration fails. This error is the error returned by the server
         */
        async register(email: string, password: string, username: string): Promise<boolean> {
            return true;
        },

        /**
         * Refreshes the access token by sending the refresh token to the server. The new access token is stored in a cookie. The refresh token is also updated in a cookie. The authentication status is set to AUTHENTICATED
         * @throws {Error} If the refresh fails. This error is the error returned by the server
         */
        async refreshAuth(): Promise<void> {
            this.status = AuthenticationStatus.PENDING;
            const refreshTokenCookie = useCookie('refresh_token');

            if (!(typeof refreshTokenCookie.value === 'string')) {
                return;
            }

            try {
                await $fetch('/api/token/refresh', {
                    method: 'POST',
                    body: JSON.stringify({ refresh: refreshTokenCookie.value }),
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': await this.getCsrfToken(),
                    },

                    onResponse: ({ response }) => {
                        if (response.status === 200) {
                            const { access, refresh } = response._data;
                            useCookie('access_token').value = access;
                            refreshTokenCookie.value = refresh;
                            this.status = AuthenticationStatus.AUTHENTICATED;
                        }
                    },
                });
            } catch (error) {
                this.status = AuthenticationStatus.UNAUTHENTICATED;
                this.logout();
                useRouter().push('/login');
                throw error;
            }
        },

        /**
         * Checks if the user is authenticated by verifying the access token with the server. The authentication status is set to AUTHENTICATED if the token is valid
         * @returns {boolean} True if the user is authenticated, false otherwise
         */
        async isAuthenticated(): Promise<boolean> {
            this.status = AuthenticationStatus.PENDING;

            if (this.isAuthExpired()) {
                await this.refreshAuth();
            }

            await $fetch('/api/token/verify', {
                method: 'POST',
                body: {
                    token: useCookie('access_token').value,
                },
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': await this.getCsrfToken(),
                },

                onResponse: ({ response }) => {
                    if (response.status === 200) {
                        this.status = AuthenticationStatus.AUTHENTICATED;
                    }
                },
            });
            // @ts-ignore
            return this.status === AuthenticationStatus.AUTHENTICATED;
        },

        /**
         * Checks if the access token is expired
         * @returns {boolean} True if the token is expired, false otherwise
         */
        isAuthExpired(): boolean {
            const token = useCookie('access_token').value;

            if (!(typeof token === 'string')) {
                return true;
            }

            try {
                const decoded = jwtDecode(token);
                return (decoded.exp as number) < Date.now() / 1000;
            } catch (error) {
                return true;
            }
        },

        /**
         * Gets a CSRF token from the server. If the token is already stored in a cookie, it is returned. Otherwise, a new token is requested from the server.
         * @returns A CSRF token.
         */
        async getCsrfToken(): Promise<string> {
            const csrfTokenCookie = useCookie('csrf_token');
            if (typeof csrfTokenCookie.value === 'string') {
                return csrfTokenCookie.value;
            } else {
                await $fetch('/api/csrf', {
                    method: 'GET',
                    onResponse: ({ response }) => {
                        this.csrfToken = response._data.csrf_token;
                    },
                }).catch((error) => {
                    useErrorDialogStore().showErrorDialog({
                        message: 'An error occurred while generating the CSRF token',
                    });
                });
            }

            return this.csrfToken as string;
        },
    },
});
