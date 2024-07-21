<script setup>

import { reactive, ref } from 'vue';
import axios from 'axios';

const form = reactive({
  username: '',
  email: '',
  password: '',
});

let waitingForCode = ref(false);
let code = ref('');
let loginToggled = ref(true);

function showError(message) {
  const error = document.querySelector('.error');
  error.innerHTML = message;
  error.style.display = 'block';
}

function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  return emailRegex.test(email);
}

async function handleRegistration() {

  if (form.username === '' || form.email === '' || form.password === '') {
    showError('Please fill in all fields');
    return;
  }

  if (form.password.length < 8) {
    showError('Password must be at least 8 characters');
    return;
  }

  if (form.username.length < 3 || form.username.length > 20) {
    showError('Username must be at least 3 characters and at most 20 characters');
    return;
  }

  const passwordRegex = /^(?=.*[!@#$%^&*§])(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

  if (!passwordRegex.test(form.password)) {
    showError('Password must contain at least one special character (!@#$%^&*§), one uppercase letter, one lowercase letter, and one number');
    return;
  }


  if (!validateEmail(form.email)) {
    showError('Invalid email');
    return;
  }



  if (!/^[a-zA-Z0-9_]+$/.test(form.username)) {
    showError('Username must consist of alphanumeric characters and underscores only');
    return;
  }

  if (await existsVerificationRequest()) {
    showError('A verification request already exists for this email');
    return;
  }

  console.log(form);
  axios.post('/api/user/register', form)
    .then(response => {
      console.log(response.status);
      console.log(response.data);

      if (response.status === 200) {
        waitingForCode.value = true;
      }
    })
    .catch(error => {
      console.log(error.response.data);  // This will show the error message from the backend
      console.log(error.response.status);  // This will show the status code
      console.log(error.response.headers);  // This will show the response headers
    });
}

async function handleCodeInput() {

  if (code.value === '') {
    showError('Please fill in the code');
    return;
  }

  if (code.value.length !== 6) {
    showError('Code must be 6 characters long');
    return;
  }

  if (!/^\d+$/.test(code.value)) {
    showError('Code must contain only numbers');
    return;
  }

  axios.post('/api/user/verify', { code: code.value, email: form.email, type: 1 })
    .then(response => {
      console.log(response.status);
      console.log("Hier sollte ein User sein", response.data);

      if (response.status === 200) {
        waitingForCode.value = false;
      }
    })

    .catch(error => {
      console.log(error.response.data);  // This will show the error message from the backend
      console.log(error.response.status);  // This will show the status code
      console.log(error.response.headers);  // This will show the response headers
    });
}

async function handleLogin() {
  if (form.email === '' || form.password === '') {
    showError('Please fill in all fields');
    return;
  }

  if (!validateEmail(form.email)) {
    showError('Invalid email');
    return;
  }

  axios.post('/api/user/login', form)
    .then(response => {
      console.log(response.status);
      console.log(response.data);

      if (response.status === 200) {
        console.log("Successfully logged in");
      }
    })
    .catch(error => {
      console.log(error.response.data);  // This will show the error message from the backend
      console.log(error.response.status);  // This will show the status code
      console.log(error.response.headers);  // This will show the response headers
    });

}

async function existsVerificationRequest() {
  try {
    const response = await axios.post('/api/user/verify/exists', { email: form.email, type: 1 });
    console.log(response.status);
    if (response.status === 200) {
      return response.data.exists;
    }
  } catch (error) {
    console.log(error.response.data);  // This will show the error message from the backend
    console.log(error.response.status);  // This will show the status code
    console.log(error.response.headers);  // This will show the response headers
  }
}

</script>

<template>
  <form v-if="loginToggled" @submit.prevent="handleLogin">
    <input type="email" placeholder="Email" v-model="form.email">
    <input type="password" placeholder="Password" v-model="form.password">
    <button type="submit">Login</button>
    <p class="error" style="display: none;"></p>
    <p>Don't have an account? <a href="#" @click="loginToggled = false">Register</a></p>
  </form>

  <form v-else-if="!login && !waitingForCode" @submit.prevent="handleRegistration">
    <input type="text" placeholder="Username" v-model="form.username">
    <input type="email" placeholder="Email" v-model="form.email">
    <input type="password" placeholder="Password" v-model="form.password">
    <button type="submit">Register</button>
    <p class="error" style="display: none;"></p>
    <p>Already have an account? <a href="#" @click="loginToggled = true">Login</a></p>
  </form>

  <form v-else @submit.prevent="handleCodeInput">
    <input type="text" placeholder="Code Input" v-model="code">
    <button type="submit">Submit</button>
    <p class="error" style="display: none;"></p>
  </form>
</template>

<style scoped>
body {
  font-family: Arial, sans-serif;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
}

input {
  margin-bottom: 10px;
  padding: 5px;
}

button {
  padding: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
}
</style>