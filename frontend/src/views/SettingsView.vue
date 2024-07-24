<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { getEmailByToken, checkAuth } from '@/utils/rest/Users';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import { useRouter } from 'vue-router';

const toast = useToast();
const router = useRouter();

onMounted(() => {
  checkAuth(router);
});

const waiting = {
  changeEmail: ref(false),
  changeUsername: ref(false),
  changePassword: ref(false),
  deleteAccount: ref(false)
};

const changePasswordCode = ref('');

async function changeEmail() {
  console.log('changeEmail');
}

async function changeUsername() {
  try {
    const email = await getEmailByToken(localStorage.getItem('access_token'));
    const response = await axios.post('/api/user/change-username', {
      new_username: newUsername.value,
      email: email
    });

    if (response.status === 200) {
      toast.success('Username changed successfully');
    } else {
      toast.error('Username could not be changed');
    }
  } catch (error) {
    console.error(error);
  }
}

async function changePassword() {
  try {
    const email = await getEmailByToken(localStorage.getItem('access_token'));
    const response = await axios.post('/api/user/change-password', {
      email: email,
      new_password: newPassword.value
    });

    if ((await response.status) === 200) {
      toast.success('Password change request sent');
    } else {
      toast.error('Password change request could not be sent');
    }
  } catch (error) {
    console.error(error);
  }
}

async function deleteAccount() {
  console.log('deleteAccount');
}

const newEmail = ref('');
const newUsername = ref('');
const currentPassword = ref('');
const newPassword = ref('');
const repeatNewPassword = ref('');
const confirmDelete = ref(false);
</script>

<template>
  <div>
    <h1>Settings</h1>
  </div>

  <div>
    <h2>Change Email</h2>
    <form>
      <label for="email">New Email:</label>
      <input type="email" id="email" name="email" v-model="newEmail" />
      <button @click="changeEmail">Submit</button>
    </form>

    <h2>Change Username</h2>
    <form @submit.prevent="changeUsername">
      <label for="username">New Username:</label>
      <input
        type="text"
        id="username"
        name="username"
        placeholder="New Username"
        v-model="newUsername"
      />
      <button type="submit">Submit</button>
    </form>

    <h2>Change Password</h2>
    <form v-if="!waiting.changePassword.value" @submit.prevent="changePassword">
      <label for="currentPassword">Current Password:</label>
      <input
        type="password"
        id="currentPassword"
        name="currentPassword"
        v-model="currentPassword"
      />
      <label for="newPassword">New Password:</label>
      <input type="password" id="newPassword" name="newPassword" v-model="newPassword" />
      <label for="repeatNewPassword">Repeat New Password:</label>
      <input
        type="password"
        id="repeatNewPassword"
        name="repeatNewPassword"
        v-model="repeatNewPassword"
      />
      <button type="submit">Submit</button>
    </form>
    <form v-else>
      <label for="changePasswordCode">Enter Code:</label>
      <input
        type="text"
        id="changePasswordCode"
        name="changePasswordCode"
        v-model="changePasswordCode"
      />
      <button @click="changePassword">Submit</button>
    </form>

    <h2>Delete Account</h2>
    <form v-if="!waiting.deleteAccount.value">
      <label for="confirmDelete">Confirm Account Deletion:</label>
      <input type="checkbox" id="confirmDelete" name="confirmDelete" v-model="confirmDelete" />
      <button @click="deleteAccount">Submit</button>
    </form>
  </div>
</template>

<style>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

form {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  margin-bottom: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

button {
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
