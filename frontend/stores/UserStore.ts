import type { CookieRef } from '#app';
import { defineStore } from 'pinia';

export const useUserStore = defineStore({
    id: 'userStore',
    state: () => ({
        loggedIn: false,
        lastFetched: null as Date | null,

        // Values from the profile
        username: '',
        email: '',
        isActive: false,
        isStaff: false,
        isSuperuser: false,
        groups: [] as string[],
        permissions: [] as string[],
        dateJoined: null as Date | null,
        lastLogin: null as Date | null,
        timezone: '',
        timeformat: '',
    }),
    actions: {
        initUser(): void {
            useCookie('timezone').value = getCurrentTimezone();
        },

        async fetchUser(): Promise<void> {
            this.lastFetched = new Date();

            try {
                const profileResponse: Response = await fetch(
                    '/api/users/profile',
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': useCsrf().getToken(),
                            Authorization: `Bearer ${useCookie('access_token').value}`,
                        },
                    }
                );

                if (profileResponse.status === 200) {
                    this.loggedIn = true;

                    const profileData = await profileResponse.json();
                    this.username = profileData.username;
                    this.email = profileData.email;
                    this.isActive = profileData.is_active;
                    this.isStaff = profileData.is_staff;
                    this.isSuperuser = profileData.is_superuser;
                    this.groups = profileData.groups;
                    this.permissions = profileData.permissions;
                    this.dateJoined = new Date(profileData.date_joined);
                    this.lastLogin = new Date(profileData.last_login);
                    this.timezone = profileData.timezone;
                    this.timeformat = profileData.timeformat;
                }
            } catch (error: any) {
                console.error(
                    `An unexpected error occurred while fetching the profile: ${(error as Error).message}`
                );
            }
        },
    },
});
