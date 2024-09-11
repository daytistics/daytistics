<template>
  <div>
    <nav class="flex flex-row justify-between shadow-sm bg-green-600 text-white">
      <div class="flex flex-row gap-6">
        <img src="/assets/graphics/images/logo.png" width="75px" class="ml-8" />
        <ul class="flex flex-row justify-around align-middle items-center gap-3 pl-0 p-5">
          <li>Features</li>
          <li>Docs</li>
          <li>About</li>
        </ul>
      </div>

      <div>
        <ul class="flex flex-row justify-around align-middle items-center gap-3 p-5">
          <li v-if="!isAuthenticated">
            <NuxtLink to="/users/register">
              Sign Up
            </NuxtLink>
          </li>
          <li v-if="!isAuthenticated">
            <NuxtLink to="/users/login">
              Log In
            </NuxtLink>
          </li>
          <li v-if="isAuthenticated">
            <NuxtLink to="/dashboard">
              Dashboard
            </NuxtLink>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script lang="ts" setup>
const open = ref(false);
const userMenuOpen = ref(false);
var isAuthenticated = ref(false);

onMounted(async () => {
  isAuthenticated.value = await useUser().isAuthenticated();
});
</script>

<style></style>