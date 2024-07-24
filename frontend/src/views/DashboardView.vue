<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterLink, useRouter } from 'vue-router';
import { checkAuth } from '@/utils/rest/Users';

const router = useRouter();

onMounted(() => {
  checkAuth(router);
});
</script>

<template>
  <div>
    <h1>Dashboard</h1>
    <RouterLink to="/settings">Zu den Einstellungen</RouterLink>
  </div>
</template>
