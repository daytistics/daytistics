<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { getEmailByToken, checkAuthRejection, isUserVerified } from '@/utils/rest/users';
import { routesContainer } from '@/router/routes';

const router = useRouter();

const form = reactive({
  username: '',
  email: '',
  password: ''
});

let waitingForCode = ref(false);
let code = ref('');
let loginToggled = ref(true);
let isErrorThrown = ref(false);
let errorText = ref('');

onMounted(async () => {
  if (localStorage.getItem('access_token') && localStorage.getItem('refresh_token') && await isUserVerified()) {
    router.push('/dashboard');
  } else if (localStorage.getItem('access_token') && localStorage.getItem('refresh_token') && !await isUserVerified()) {
    waitingForCode.value = true;
    loginToggled.value = false;
  } else {
    checkAuthRejection(router);
  }
});

function showError(message: string) {
  errorText.value = message;
  isErrorThrown.value = true;
}

function validateEmail(email: string) {
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
    showError(
      'Password must contain at least one special character (!@#$%^&*§), one uppercase letter, one lowercase letter, and one number'
    );
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

  // // TODO: Fix this 
  // if (await isUserExisting(form.email)) {
  //   showError('User with this email already exists');
  //   return;
  // }

  console.log(form);
  axios
    .post(routesContainer.REGISTER_USER, form)
    .then((response) => {
      console.log(response.status);
      console.log(response.data);

      if (response.status === 201) {
        waitingForCode.value = true;

        (async () => {
          try {
            const response = await axios.post(routesContainer.LOGIN_USER, {
              email: form.email,
              password: form.password
            });
            console.log(response.status);
            console.log(response.data);

            if (response.status === 200) {
              let access_token = response.data.content[0].access_token;
              let refresh_token = response.data.content[0].refresh_token;

              localStorage.setItem('access_token', access_token);
              localStorage.setItem('refresh_token', refresh_token);
            }
          } catch (error: any) {
            console.log(error.response.data); 
            console.log(error.response.status); 
            console.log(error.response.headers); 
          }
        })();

      }
    })
    .catch((error) => {
      console.log(error.response.data); // This will show the error message from the backend
      console.log(error.response.status); // This will show the status code
      console.log(error.response.headers); // This will show the response headers
    });
}

async function handleCodeSubmit() {

  code.value = code.value.trim();

  if (code.value === '') {
    showError('Bitte gib einen Code ein');
    return;
  }

  if (!/^\d+$/.test(code.value)) {
    showError('Der Code darf nur aus Zahlen bestehen');
    return;
  }

  if (code.value.length !== 6) {
    showError('Der Code muss 6 Zahlen lang sein');
    return;
  }

  axios
    .post(routesContainer.VERIFY_REGISTRATION, { code: code.value, email: form.email })
    .then((response) => {
      console.log(response.status);

      if (response.status === 200) {
        waitingForCode.value = false;
        router.push('/dashboard');
      }
    })

    .catch((error) => {
      // I know this is a bad practice, but I'm not sure how to handle this properly
      
      if (error.response.status === 404) {
        showError('Es wurde keine Registrierungsanfrage gefunden');
        return;
      } else if (error.response.status === 601) {
        router.push('/auth/rejected');
        return;
      } else if (error.response.status === 602) {
        showError('Der Code wurde aus Sicherheitsgründen entwertet, bitte fordere einen neuen an');
        return;
      } else if (error.response.status === 603) {
        showError('Der Code ist abgelaufen');
        return;
      }
    })
}

async function handleLogin() {
  console.log(form);
  try {
    const response = await axios.post(routesContainer.LOGIN_USER, {
      email: form.email,
      password: form.password
    });
    console.log(response.status);

    if (response.status === 200) {
      let access_token = response.data[0].access_token;
      let refresh_token = response.data.conte.contentnt[0].refresh_token;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      router.push('/dashboard');
    }
  } catch (error: any) {
    showError('Invalid credentials');
    console.log(error.response.data); 
    console.log(error.response.status); 
    console.log(error.response.headers);
  }
}

async function resendRegistrationCode() {
  try {
    const email = await getEmailByToken();
    const response = await axios.post(routesContainer.RESEND_VERIFICATION_EMAIL, {
      email: email
    });
    console.log(response.status);

  } catch (error: any) {
    console.log(error.response.data); 
    console.log(error.response.status); 
    console.log(error.response.headers); 
  }

}

</script>

<template>
  <form v-if="loginToggled" @submit.prevent="handleLogin">
    <input type="email" placeholder="Email" v-model="form.email" />
    <input type="password" placeholder="Password" v-model="form.password" />
    <button type="submit">Login</button>
    <p v-if="isErrorThrown" class="error">{{ errorText }}</p>
    <p>Don't have an account? <a href="#" @click="loginToggled = false">Register</a></p>
  </form>

  <form v-else-if="!loginToggled && !waitingForCode" @submit.prevent="handleRegistration">
    <input type="text" placeholder="Username" v-model="form.username" />
    <input type="email" placeholder="Email" v-model="form.email" />
    <input type="password" placeholder="Password" v-model="form.password" />
    <button type="submit">Register</button>
    <p v-if="isErrorThrown" class="error">{{ errorText }}</p>
    <p>Already have an account? <a href="#" @click="loginToggled = true">Login</a></p>
  </form>

  <form v-else @submit.prevent="handleCodeSubmit">
    <input type="text" placeholder="Code Input" v-model="code" />
    <button type="submit">Submit</button>
    <a href="#" @click="resendRegistrationCode">Click here to receive a new code</a>
    <p v-if="isErrorThrown" class="error">{{ errorText }}</p>
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
