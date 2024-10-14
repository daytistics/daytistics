<!-- <template>
  <div class="">
    <div class="rounded-md p-2 bg-white">
      <div class="flex items-center justify-center my-3">
        <div class="xl:mx-auto shadow-md p-4 xl:w-full xl:max-w-sm 2xl:max-w-md card">
          <div class="mb-2"></div>
          <h2 class="text-2xl font-bold leading-tight">
            Log in to your account
          </h2>
          <p class="mt-2 text-base text-gray-600">
            Don't have an account? <NuxtLink to="/auth/register" class="text-secondary">Sign up</NuxtLink>
          </p>

          <form @submit.prevent="loginUser" class="mt-5">
            <div class="space-y-4">

              <p class="text-red-500 text-sm" id="login-error">
                {{ loginError }}
              </p>
              <div>
                <label class="text-base font-medium text-gray-900">
                  Email address
                </label>
                <div class="mt-2">
                  <input placeholder="Email" type="email" required
                    class="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                    v-model="email" name="email" />
                </div>
              </div>
              <div>
                <div class="flex items-center justify-between">
                  <label class="text-base font-medium text-gray-900">
                    Password
                  </label>
                </div>
                <div class="mt-2">
                  <input placeholder="Password" type="password" required
                    class="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                    v-model="password" name="password" />
                </div>
              </div>
              <div>
                <button
                  class="inline-flex w-full items-center justify-center font-semibold leading-7 button bg-secondary hover:bg-secondary-dark"
                  type="submit">
                  Log In
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

</template> -->

<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-lg shadow-xl overflow-hidden">
      <div class="p-6 sm:p-8">
        <div class="flex justify-center mb-8">
          <img src="/assets/graphics/images/logo.png" alt="Logo" class="h-12 w-auto" />
        </div>
        <h2 class="text-2xl font-bold text-center text-gray-700 mb-6">Log in to your account</h2>
        <form @submit.prevent="form.submit" class="space-y-6">
          <div>
            <label for="email" class="text-sm font-medium text-gray-700 block mb-2">Email address</label>
            <input id="email" v-model="form.email.value" type="email" required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent" />
          </div>
          <div>
            <div>
              <label for="password" class="text-sm font-medium text-gray-700 block mb-2">Password</label>
              <input id="password" v-model="form.password.value" type="password" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent" />

            </div>
            <div class="text-sm flex flex-row justify-end pt-2">
              <a href="#" class=" font-normal text-green-600 hover:text-green-500">Forgot your password?</a>
            </div>
          </div>
          <div>
            <button type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-300">
              Log In
            </button>
          </div>
        </form>
      </div>
      <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 sm:px-8">
        <p class="text-xs leading-5 text-gray-500">
          Don't have an account?
          <a href="#" class="font-medium text-green-600 hover:text-green-500">Sign up</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>


const auth = useAuth();

const { update: updateUser } = useUserStore();
const { showErrorModal } = useErrorModalStore();

const form = useForm();
const loginAPI = useLoginAPI();

onMounted(async () => {
  if (await auth.verifyAuth()) {
    updateUser();
    useRouter().push('/dashboard');
  }
});

function useForm() {
  const email = ref<string>('');
  const password = ref<string>('');

  const submit = async () => {
    loginAPI.login(email.value, password.value);
    updateUser();
  };

  return {
    email,
    password,
    submit,
  };
}

function useLoginAPI() {
  const { $api } = useNuxtApp();
  const login = async (email: string, password: string) => {
    try {
      await $api('/api/users/login', {
        method: 'POST',
        body: {
          email,
          password,
        },
        onResponse: ({ request, response, options }) => {
          if (response.status === 200) {
            const accessToken = response._data.accessToken;
            const refreshToken = response._data.refreshToken;

            const accessTokenCookie = useCookie("access_token");
            const refreshTokenCookie = useCookie("refresh_token");

            accessTokenCookie.value = accessToken;
            refreshTokenCookie.value = refreshToken;

            useRouter().push('/dashboard');
          }
        },
      });
    } catch (error: any) {
      showErrorModal({
        message: 'An error occurred while logging in.',
        error: error.data.detail,
      });
    }
  };

  return {
    login,
  };
}

</script>