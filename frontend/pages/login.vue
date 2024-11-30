<template>
    <div class="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 p-4">
        <GoBackButton
            to="/"
            class="p-2"
        />
        <div class="flex items-center justify-center min-h-screen">
            <div class="max-w-md w-full bg-white rounded-lg shadow-xl overflow-hidden">
                <div class="p-6 sm:p-8">
                    <div class="flex justify-center mb-8">
                        <NuxtImg
                            src="/images/logo.png"
                            alt="Logo"
                            class="h-12 w-auto"
                        />
                    </div>
                    <h2 class="text-2xl font-bold text-center text-gray-700 mb-6">
                        Log in to your account
                    </h2>
                    <form
                        @submit.prevent="form.submit"
                        class="space-y-6"
                    >
                        <div>
                            <label
                                for="email"
                                class="text-sm font-medium text-gray-700 block mb-2"
                                >Email address</label
                            >
                            <input
                                id="email"
                                v-model="form.email.value"
                                type="email"
                                required
                                class="min-w-96 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <div>
                                <label
                                    for="password"
                                    class="text-sm font-medium text-gray-700 block mb-2"
                                    >Password</label
                                >
                                <input
                                    id="password"
                                    v-model="form.password.value"
                                    type="password"
                                    required
                                    class="min-w-96 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                />
                            </div>
                            <div class="text-sm flex flex-row justify-end pt-2">
                                <a
                                    href="#"
                                    class="font-normal text-green-600 hover:text-green-500"
                                    >Forgot your password?</a
                                >
                            </div>
                        </div>
                        <div>
                            <button
                                type="submit"
                                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-300"
                            >
                                Log In
                            </button>
                        </div>
                    </form>
                </div>
                <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 sm:px-8">
                    <p class="text-xs leading-5 text-gray-500">
                        Don't have an account?
                        <NuxtLink
                            to="/signup"
                            class="font-medium text-green-600 hover:text-green-500"
                            >Sign up
                        </NuxtLink>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useToast } from 'vue-toastification';

const form = useForm();
const loginAPI = useLoginAPI();

function useForm() {
    const email = ref<string>('');
    const password = ref<string>('');

    const submit = async () => {
        loginAPI.login(email.value, password.value);
    };

    return {
        email,
        password,
        submit,
    };
}

function useLoginAPI() {
    const login = async (email: string, password: string) => {
        try {
            await useAuthStore().login(email, password);
            await navigateTo('/dashboard');
        } catch (error: any) {
            useToast().error(error.data.detail);
        }
    };

    return {
        login,
    };
}
</script>
