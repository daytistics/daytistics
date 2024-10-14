<template>
  <footer class="w-full border-t border-gray-200">
    <div class="flex flex-col justify-between p-9 md:flex-row text-center items-center align-middle">
      <div class="md:mr-9 flex flex-col justify-center align-middle items-center">
        <span>Made with ☕ and ❤️ by the Open-Source-Community</span>
      </div>
      <div class="md:mr-9 flex flex-row justify-center align-middle items-center gap-4">
        <NuxtLink to="/licenses.txt" external>Licenses</NuxtLink>
        <span class="hover:cursor-not-allowed">Privacy</span>
        <span class="hover:cursor-not-allowed">Terms of use</span>
        <NuxtLink to="/legal/imprint">Imprint</NuxtLink>
      </div>
    </div>
  </footer>
</template>