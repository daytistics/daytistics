<template>

  <ErrorModal />
  <InfoModal />


  <div class="flex flex-col min-h-screen">
    <Navbar />

    <!-- <div id="early-stage" class="flex items-center p-4 text-green-800 rounded-lg bg-green-200" role="alert">
      <svg class="flex-shrink-0 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
        viewBox="0 0 20 20">
        <path
          d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z" />
      </svg>
      <div class="ms-3 text-sm font-medium">
        Welcome to the proof of concept of Daytistics! Thank you for testing it out. We would love to hear your
        <NuxtLink to="/feedback" class="underline">feedback</NuxtLink>.
      </div>
    </div> -->

    <div class="flex-1">
      <slot />
    </div>
    <Footer />
  </div>
</template>

<script lang="ts" setup>

import { initDismisses } from 'flowbite';

const infoModalStore = useInfoModalStore();
const { showInfoModal } = infoModalStore;

function openInfoModal() {
  const content = `
    Hello! 👋 Welcome to Daytistics. <br>
    We are really glad that you made it here. 
    Unfortunately, you will not be able to log in or sign up as we are currently only online for development purposes.
    <br>
    We would love to meet you again on this page in a few months, if our project goes into production.
    <br>
    If you are interested in speeding up the process, you can contribute on <a target="_blank" href="https://github.com/daytistics/daytistics" class="text-primary">Github</a> or donate to our project.    
    <br>
    <br>
    Thank you for your understanding and have a great day!
    <br>
    Yours, the Daytistics team.
  `;
  showInfoModal({
    heading: 'Welcome to Daytistics!',
    content,
  });
}

onMounted(() => {

  if (useRoute().path === '/') {
    openInfoModal();
  }

  const { update } = useUserStore();
  update();
  initDismisses();
});


</script>