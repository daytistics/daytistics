<template>
    <div
        class="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center p-4"
    >
        <div
            class="max-w-md w-full bg-white rounded-lg shadow-xl overflow-hidden"
        >
            <div class="p-6 sm:p-8">
                <div class="flex justify-center mb-8">
                    <img
                        src="/assets/graphics/images/logo.png"
                        alt="Logo"
                        class="h-12 w-auto"
                    />
                </div>
                <h2 class="text-2xl font-bold text-center text-gray-700 mb-6">
                    Activate Account
                </h2>
                <form
                    @submit.prevent="form.submit"
                    class="space-y-6"
                >
                    <div class="flex justify-center">
                        <p>Click the button below to activate your account.</p>
                    </div>

                    <div>
                        <button
                            type="submit"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-300"
                        >
                            Activate
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {
    isValidEmail,
    isValidPassword,
    isValidUsername,
} from '~/utils/validation';

const errorDialogStore = useErrorDialogStore();
const route = useRoute();
const { uidb64, token } = route.params;
const { $api } = useNuxtApp();

const form = useForm();
const activationAPI = useActivationAPI();

function useForm() {
    const submit = () => {
        activationAPI.activate(uidb64 as string, token as string);
    };

    return {
        submit,
    };
}

function useActivationAPI() {
    const activate = async (uidb64: string, token: string) => {
        try {
            await $api(`/api/users/activate/${uidb64}/${token}`, {
                method: 'GET',

                onResponse({ request, response, options }) {
                    if (response.status === 200) {
                        useRouter().push('/login');
                    }
                },

                onResponseError({ request, response, options }) {
                    errorDialogStore.showErrorDialog({
                        message:
                            'An error occurred while activating your account.',
                        error: response._data.detail,
                    });
                },
            });
        } catch (error: any) {
            errorDialogStore.showErrorDialog({
                message: 'An error occurred while activating your account.',
                error: error.data.detail,
            });
        }
    };

    return {
        activate,
    };
}
</script>
