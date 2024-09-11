<template>

  <UModal v-model="isOpen">
    <UCard :ui="{ ring: '', divide: 'divide-y divide-gray-100' }">
      <template #header>
        Hallo Welt
      </template>

      Hallo Welt

      <template #footer>
        Hallo Welt
      </template>
    </UCard>
  </UModal>

  <div class="bg-gray-100">
    <div class="min-h-screen flex">
      <Sidebar />
    </div>

    <main class="flex-1">
      <div class="py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
          <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
        </div>
      </div>
    </main>

    <CreationButton />
  </div>
</template>

<script lang="ts" setup>

onMounted(async () => {
  if (!await useUser().isAuthenticated()) {
    useRouter().push('/users/login');
  }
});

</script>

<style></style>