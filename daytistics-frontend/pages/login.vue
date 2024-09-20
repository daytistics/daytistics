<template>
  <div class="">
    <div class="rounded-md p-2 bg-white">
      <div class="flex items-center justify-center my-3">
        <div class="xl:mx-auto shadow-md p-4 xl:w-full xl:max-w-sm 2xl:max-w-md card">
          <div class="mb-2"></div>
          <h2 class="text-2xl font-bold leading-tight">
            Log in to your account
          </h2>
          <p class="mt-2 text-base text-gray-600">
            Don't have an account? <NuxtLink to="/register" class="text-secondary">Sign up</NuxtLink>
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

</template>

<script lang="ts" setup>

const eventBus = useEventBusStore();
const email = ref('');
const password = ref('');
const loginError = ref<string>('');
const csrfToken = ref('');

onMounted(async () => {
  csrfToken.value = useCsrfToken().getToken();

  if (await useUser().isAuthenticated()) {
    useRouter().push('/dashboard');
  }
});

async function loginUser() {

  await $fetch('/api/users/login/', {
    server: false,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': useCsrfToken().getToken(),
    },
    body: {
      email: email.value,
      password: password.value,
    },

    onResponse: ({ request, response, options }) => {
      if (response.status === 200) {
        console.log(response._data);

        const accessToken = response._data.accessToken;
        const refreshToken = response._data.refreshToken;

        const accessTokenCookie = useCookie("access_token");
        const refreshTokenCookie = useCookie("refresh_token");

        accessTokenCookie.value = accessToken;
        refreshTokenCookie.value = refreshToken;

        useRouter().push('/dashboard');

        eventBus.emit('user-login')

      }
    },
  });

}
</script>

<style></style>