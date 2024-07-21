<script setup>

import { onMounted, ref } from 'vue';

let isAuthenticated = ref(false);

onMounted(() => {
  const token = localStorage.getItem('token');
  if (token) {
    isAuthenticated.value = true;
  }
});

</script>