<template>

  <div>
    <section class="rounded-md p-2 bg-white">
      <div class="flex items-center justify-center my-3">
        <div class="xl:mx-auto shadow-md p-4 xl:w-full xl:max-w-sm 2xl:max-w-md">
          <div class="mb-2"></div>
          <h2 class="text-2xl font-bold leading-tight">
            Sign up to create account
          </h2>
          <p class="mt-2 text-base text-gray-600">
            <span>Already have an account? </span>
            <NuxtLink to="/auth/login" class="text-sky-600">Log in</NuxtLink>
          </p>
          <form @submit.prevent="registerUser" class="mt-5">
            <p class="text-red-500" id="error"></p>
            <div class="space-y-4">
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
                  type="submit"> Create Account </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  </div>

</template>

<script lang="ts" setup>
import { Dismiss } from 'flowbite';


const username = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('');
const csrfToken = ref('');
const inputValidation = useInputValidation();
const errorMessage = document.getElementById('error');
const auth = useAuth();

onMounted(async () => {
  csrfToken.value = useCsrf().getToken();

  if (await auth.isAuthenticated()) {
    useRouter().push('/dashboard');
  }
});

function validateInput() {
  if (!inputValidation.isValidUsername(username.value)) {
    alert('Invalid username');
  }

  if (!inputValidation.isValidEmail(email.value)) {
    alert('Invalid email');
  }

  // if (!inputValidation.isValidPassword(password1.value)) {
  //   alert('Invalid password');
  // }

  if (password1.value != password2.value) {
    alert('Passwords do not match');
  }
}


async function registerUser() {

  validateInput();

  await $fetch('/api/users/auth/register/', {
    server: false,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': useCsrf().getToken(),
    },
    body: {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    },

    onResponse({ request, response, options }) {
      if (response.status === 201) {
        useRouter().push('/auth/login');
      }
    },

  }).catch((error) => {
    console.log(error);
    if (errorMessage) {
      errorMessage.innerHTML = `${error.data.message}`;
    }

  });
}
</script>

<style></style>