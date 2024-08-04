<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterLink, useRouter } from 'vue-router';
import { isUserVerified, checkAuth } from '@/utils/rest/users';

const router = useRouter();
const isVerified = ref(false);

onMounted(async () => {

  if (localStorage.getItem('access_token') && localStorage.getItem('refresh_token') && await isUserVerified()) {
    return;
  } else if (localStorage.getItem('access_token') && localStorage.getItem('refresh_token') && !await isUserVerified()) {
    router.push('/auth');
  } else {
    checkAuth(router);
  }
});
</script>

<template>
  <div>
    <h1>Dashboard</h1>
    <RouterLink to="/settings">Zu den Einstellungen</RouterLink>
    <p style="color: lawngreen" v-if="isVerified">Du bist verifiziert!</p>
    <p style="color: red" v-else>Du bist nicht verifiziert!</p>
  </div>
</template>
