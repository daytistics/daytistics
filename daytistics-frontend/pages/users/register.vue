<template>
  <div class="">
    <section class="rounded-md p-2 bg-white">
      <div class="flex items-center justify-center my-3">
        <div class="xl:mx-auto shadow-md p-4 xl:w-full xl:max-w-sm 2xl:max-w-md">
          <div class="mb-2"></div>
          <h2 class="text-2xl font-bold leading-tight">
            Sign up to create account
          </h2>
          <p class="mt-2 text-base text-gray-600">
            <span>Already have an account? </span>
            <NuxtLink to="/users/login" class="text-sky-600">Log in</NuxtLink>
          </p>
          <form @submit.prevent="registerUser" class="mt-5">
            <div class="space-y-4">

              <ul class="text-red-500 text-sm" id="registration-error">
                <li v-if="!useInputValidation().isValidUsername(username)">Invalid username</li>
                <li v-else-if="!useInputValidation().isValidEmail(email)">Invalid email address</li>
                <li v-else-if="!useInputValidation().isValidPassword(password1)">Invalid or insecure password</li>
                <li v-else-if="password1 != password2">Passwords do not match</li>

              </ul>

              <div>
                <label class="text-base font-medium text-gray-900">
                  User Name
                </label>
                <div class="mt-2">
                  <input placeholder="Full Name" type="text"
                    class="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                    v-model="username" name="user_name" />
                </div>
              </div>
              <div>
                <label class="text-base font-medium text-gray-900">
                  Email address
                </label>
                <div class="mt-2">
                  <input placeholder="Email" type="email"
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
                  <input placeholder="Password" type="password"
                    class="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                    v-model="password1" name="password" />
                </div>
              </div>
              <div>
                <div class="flex items-center justify-between">
                  <label class="text-base font-medium text-gray-900">
                    Repeat Password
                  </label>
                </div>
                <div class="mt-2">
                  <input placeholder="Password" type="password"
                    class="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                    v-model="password2" name="password" />
                </div>
              </div>
              <div>
                <button
                  class="inline-flex w-full items-center justify-center rounded-md bg-green-600 px-3.5 py-2.5 font-semibold leading-7 text-white hover:bg-black/80"
                  type="submit"
                  :disabled="!useInputValidation().isValidUsername(username) || !useInputValidation().isValidEmail(email) || !useInputValidation().isValidPassword(password1) || password1 != password2"
                  :class="{
                    'cursor-not-allowed': !useInputValidation().isValidUsername(username) ||
                      !useInputValidation().isValidEmail(email) || !useInputValidation().isValidPassword(password1) ||
                      password1 != password2
                  }"> Create Account </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  </div>

</template>

<script lang="ts" setup>

const username = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('');
const csrfToken = ref('');
const backendErrorOccurred = ref(false);
const backendErrorMessage = ref('');

onMounted(async () => {
  csrfToken.value = useCsrfToken().getToken();

  if (await useUser().isAuthenticated()) {
    useRouter().push('/dashboard');
  }
});

async function registerUser() {

  if (password1.value != password2.value) {
    alert('Passwords do not match');
    return;
  }

  await $fetch('/api/users/register/', {
    server: false,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': useCsrfToken().getToken(),
    },
    body: {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    },

    onResponse({ request, response, options }) {
      if (response.status === 201) {
        useRouter().push('/users/login');
      }
    },

  }).catch((error) => {
    const registrationError = document.getElementById('registration-error');
    if (registrationError) {
      registrationError.innerHTML = `<li>Backend error: ${error.data.message}</li>`;
    }

  });
}
</script>

<style></style>