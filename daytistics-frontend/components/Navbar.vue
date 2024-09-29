<template>
  <div :key="navbarKey" class="shadow-sm bg-white text-darkgray text-lg border-b-0 border-darkgray">
    <nav class="flex flex-row items-center mx-auto justify-between max-w-8xl">
      <div class="flex flex-row items-center gap-6">
        <NuxtLink to="/">
          <NuxtImg src="/images/logo.png" class="ml-3 md:ml-8 h-16 w-auto md:w-75px md:h-75px" />
        </NuxtLink>
        <ul v-if="!currentUrl.includes('/dashboard')"
          class="hidden md:flex flex-row justify-around align-middle items-center gap-5 pl-0 p-5">
          <li v-for="link in navbarLinksLoggedOut" :key="currentUrl">
            <NuxtLink :to="link.href" class="flex justify-center align-middle items-center flex-row gap-1">
              <component :is="link.icon" width="15px" stroke="currentColor" />
              <span>{{ link.name }}</span>
            </NuxtLink>
          </li>
        </ul>
        <ul v-else class="hidden md:flex flex-row justify-around align-middle items-center gap-5 pl-0 p-5">
          <li v-for="link in navbarLinksLoggedIn" :key="currentUrl">
            <NuxtLink :to="link.href" class="flex justify-center align-middle items-center flex-row gap-2">
              <component :is="link.icon" stroke="currentColor" width="15px" />
              <span>{{ link.name }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>

      <div class="flex justify-center items-center mr-4">
        <svg class="block md:hidden w-10 h-10 text-gray-800 dark:text-white" xmlns="http://www.w3.org/2000/svg"
          data-drawer-target="drawer-navigation" data-drawer-show="drawer-navigation" data-drawer-placement="right"
          width="24" height="24" fill="none" viewBox="0 0 24 24">
          <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M5 7h14M5 12h14M5 17h14" />
        </svg>

        <div id="drawer-navigation"
          class="fixed top-0 right-0 z-40 h-screen p-4 overflow-y-auto transition-transform translate-x-full bg-white w-64 dark:bg-gray-800"
          tabindex="-1" aria-labelledby="drawer-navigation-label">
          <h5 id="drawer-navigation-label" class="text-base font-semibold text-gray-500 uppercase dark:text-gray-400">
            Menu</h5>
          <button type="button" data-drawer-hide="drawer-navigation" aria-controls="drawer-navigation"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 absolute top-2.5 end-2.5 inline-flex items-center justify-center dark:hover:bg-gray-600 dark:hover:text-white">
            <X stroke="currentColor" width="20px" />
            <span class="sr-only">Close menu</span>
          </button>

          <div class="py-4 overflow-y-auto">
            <ul v-if="currentUrl.includes('/dashboard')" class="space-y-2 font-medium">
              <li v-for="link in navbarLinksLoggedIn" :key="currentUrl">
                <NuxtLink :to="link.href"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <component :is="link.icon" stroke="currentColor" width="15px" />
                  <span class="ms-3">{{ link.name }}</span>
                </NuxtLink>
              </li>
              <hr />
              <li>
                <button @click="logout" data-drawer-hide="drawer-navigation"
                  class="inline-flex w-full text-start items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <LogOut stroke="currentColor" width="15px" />
                  <span class="flex-1 ms-3 whitespace-nowrap hover:cursor-pointer">Sign Out</span>
                </button>
              </li>
            </ul>
            <ul v-else class="space-y-2 font-medium">
              <li v-for="link in navbarLinksLoggedOut" :key="currentUrl">
                <NuxtLink :to="link.href"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <component :is="link.icon" stroke="currentColor" width="15px" />
                  <span class="ms-3">{{ link.name }}</span>
                </NuxtLink>
              </li>

              <hr />
              <li>
                <NuxtLink to="/auth/login" :key="currentUrl"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <LogIn stroke="currentColor" width="15px" />
                  <span class="flex-1 ms-3 whitespace-nowrap">Sign In</span>
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/auth/register" :key="currentUrl"
                  class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <FilePen stroke="currentColor" width="15px" />
                  <span class="flex-1 ms-3 whitespace-nowrap">Sign Up</span>
                </NuxtLink>
              </li>
            </ul>
          </div>
        </div>

        <ul class="hidden md:flex flex-row justify-around align-middle items-center gap-3 p-5">
          <li v-if="!isAuthenticated" :key="currentUrl">
            <NuxtLink to="/auth/register">
              <button class="button bg-primary hover:bg-primary-dark">
                Sign Up
              </button>
            </NuxtLink>
          </li>
          <li v-if="!isAuthenticated" :key="currentUrl">
            <NuxtLink to="/auth/login">
              <button class="button bg-primary hover:bg-primary-dark">
                Log In
              </button>
            </NuxtLink>
          </li>
          <li v-if="isAuthenticated && !currentUrl.includes('/dashboard')" :key="currentUrl">
            <NuxtLink to="/dashboard">
              <button class="button bg-primary hover:bg-primary-dark">
                Dashboard
              </button>
            </NuxtLink>
          </li>
          <li v-else-if="isAuthenticated && currentUrl.includes('/dashboard')" :key="currentUrl + 'logout'">
            <button class="button bg-primary hover:bg-primary-dark" @click="logout">
              Log Out
            </button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script lang="ts" setup>
import { initDrawers, initDropdowns } from 'flowbite';
import { LogOut, X, FilePen, ChartNoAxesColumn, House, Brain, Settings, Telescope, BadgeDollarSignIcon, Server, Users2, Paperclip, LogIn } from 'lucide-vue-next';

const currentUrl = computed(() => useRoute().path);
const navbarKey = ref<number>(0);
const logout = () => 3;
const isAuthenticated = ref<boolean>(false);
const auth = useAuth();

const navbarLinksLoggedIn = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: House,
  },
  {
    name: 'Relationships',
    href: '/dashboard/relationships',
    icon: ChartNoAxesColumn,
  },
  {
    name: 'Models',
    href: '/dashboard/models',
    icon: Brain,
  },
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: Settings,
  },
];

const navbarLinksLoggedOut = [
  {
    name: 'Features',
    href: '/#features',
    icon: Telescope,
  },
  {
    name: 'Pricing',
    href: '/#pricing',
    icon: BadgeDollarSignIcon,
  },
  {
    name: 'Self-Hosting',
    href: '/#self-hosting',
    icon: Server,
  },
  {
    name: 'About',
    href: '/#about',
    icon: Users2,
  },
  {
    name: 'Docs',
    href: 'https://docs.daytistics.com/',
    icon: Paperclip,
  },
];

onMounted(async () => {
  isAuthenticated.value = await auth.isAuthenticated();
  initDrawers();
});
</script>

<style></style>