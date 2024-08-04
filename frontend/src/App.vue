<script setup>
import { useRouter } from 'vue-router';
import { tryRefreshToken } from './utils/rest/users';

const router = useRouter();

router.beforeEach(async (to, from, next) => {
  console.log('beforeEach');
  await tryRefreshToken();
  next();
});

</script>

<template>
  <RouterView />
</template>
