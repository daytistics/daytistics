import axios from 'axios';

async function getEmailByToken(accessToken: string) {
  try {
    const response = await axios.get('/api/user/token/email', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    const email = response.data.email as string;
    return email;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function checkAuth(router: any) {
  const refreshToken = localStorage.getItem('refresh_token');
  console.log(refreshToken);
  try {
    const response = await axios.post(
      '/api/user/token/refresh',
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`
        }
      }
    );
    if (response.status === 200) {
      const accessToken = response.data.access_token;
      localStorage.setItem('access_token', accessToken);
      console.log('Token refreshed');
    } else {
      router.push({ path: '/' });
    }
  } catch (error) {
    console.error(error);
    router.push({ path: '/' });
  }
}

async function getUserInformation(accessToken: string) {
  try {
    const response = await axios.get('/api/user', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function isUserVerified(accessToken: string) {
  try {
    const response = await getUserInformation(accessToken);
    const verification = response.verification;
    return verification === 'done';
  } catch (error) {
    console.error(error);
    return false;
  }
}

async function isUserExisting(email: string) {
  try {
    const response = await axios.post('/api/user/exists', { email: email });
    const exists = response.data.exists as boolean;
    return exists;
  } catch (error) {
    console.error(error);
    return false;
  }
}

export { getEmailByToken, checkAuth, getUserInformation, isUserVerified, isUserExisting };
