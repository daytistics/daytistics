<template>
    <div
        class="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center p-4"
    >
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
                    Sign up to create account
                </h2>
                <form
                    @submit.prevent="form.submit"
                    class="space-y-6"
                >
                    <div>
                        <label class="text-base font-medium text-gray-900"> User Name </label>
                        <div class="mt-2">
                            <input
                                placeholder="Full Name"
                                type="text"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                v-model="form.username.value"
                                name="user_name"
                            />
                        </div>
                    </div>
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
                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                    </div>
                    <div>
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-medium text-gray-700 block mb-2">
                                Password
                            </label>
                        </div>
                        <div class="mt-2">
                            <input
                                placeholder="Password"
                                type="password"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                v-model="form.password1.value"
                                name="password"
                            />
                        </div>
                    </div>
                    <div>
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-medium text-gray-700 block mb-2">
                                Repeat Password
                            </label>
                        </div>
                        <div class="mt-2">
                            <input
                                placeholder="Password"
                                type="password"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                v-model="form.password2.value"
                                name="password"
                            />
                        </div>
                    </div>
                    <div>
                        <button
                            type="submit"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-300"
                        >
                            Sign Up
                        </button>
                    </div>
                </form>
            </div>
            <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 sm:px-8">
                <p class="text-xs leading-5 text-gray-500">
                    Already have an account?
                    <a
                        href="/login"
                        class="font-medium text-green-600 hover:text-green-500"
                        >Log In</a
                    >
                </p>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { isValidPassword, isValidUsername } from '~/utils/validation';

const { showErrorDialog } = useErrorDialogStore();

const form = useForm();
const registerAPI = useRegisterAPI();

function useForm() {
    const username = ref('');
    const password1 = ref('');
    const password2 = ref('');
    const email = ref('');

    const submit = () => {
        if (!validate()) return;
        registerAPI.register();
    };

    const validate = () => {
        if (!isValidUsername(username.value)) {
            showErrorDialog({
                message:
                    'Please enter a valid username. It must be at least 4 characters long and contain only alphanumeric characters.',
            });
            return false;
        }

        if (!isValidPassword(password1.value)) {
            showErrorDialog({
                message:
                    'Please enter a valid password. It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.',
            });
            return false;
        }

        if (password1.value != password2.value) {
            showErrorDialog({
                message: 'The passwords do not match.',
            });
            return false;
        }

        return true;
    };

    return {
        username,
        password1,
        password2,
        email,
        submit,
    };
}

function useRegisterAPI() {
    const { $api } = useNuxtApp();

    const register = async () => {
        await $api('/api/users/register', {
            server: false,
            method: 'POST',
            body: {
                username: form.username.value,
                email: form.email.value,
                password1: form.password1.value,
                password2: form.password2.value,
            },

            onResponse({ request, response, options }) {
                if (response.status === 201) {
                    useRouter().push('/login');
                }
            },
        }).catch((error) => {
            console.log(error);
            showErrorDialog({
                message: 'An error occurred while registering your account.',
                error: error.data.message,
            });
        });
    };

    return { register };
}
</script>
