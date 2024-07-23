<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

let isAuthenticated = ref(false)

async function checkAuth() {
  const refreshToken = localStorage.getItem('refresh_token')
  console.log(refreshToken)
  try {
    const response = await axios.post(
      '/api/user/token/refresh',
      {}, // leerer Body
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`
        }
      }
    )
    if (response.status === 200) {
      isAuthenticated.value = true
      const accessToken = response.data.access_token
      localStorage.setItem('access_token', accessToken)
      console.log('Token refreshed')
    } else {
      isAuthenticated.value = false
    }
  } catch (error) {
    console.error(error)
    isAuthenticated.value = false
  }
}

onMounted(() => {
  checkAuth()
})
</script>

<template>
  <div>
    <h1>Dashboard</h1>
    <div v-if="isAuthenticated">
      <p>Du bist eingeloggt! :D</p>
    </div>
    <div v-else>
      <p>Du bist nicht eingeloggt!</p>
    </div>
  </div>
</template>
