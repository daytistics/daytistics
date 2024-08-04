import axios from 'axios';
import { routesContainer } from '@/router/routes';

async function getEmailByToken() {
  try {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.get(routesContainer.GET_USER_EMAIL, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    const email = response.data.content[0].email as string;
    return email;
  } catch (error: any) {
    if (error.response && error.response.status === 401) {
      console.error('Unauthorized. Try to refresh token by logging in again. We are sorry for the inconvenience.');
    }
    return null;
  }
}

async function checkAuthRejection(router: any) {
  if (await hasAuthRejection()) {
    router.push({ path: '/auth/rejected'});
    return;
  }
}

async function tryRefreshToken() {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await axios.post(
      routesContainer.REFRESH_USER_TOKEN,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`
        }
      }
    );
    if (response.status === 200) {
      const accessToken = response.data.content[0].access_token;
      localStorage.setItem('access_token', accessToken);
      console.log('Token refreshed');
    }
  } catch (error) {
    console.error(error);
  }
}

async function checkAuth(router: any) {
  const refreshToken = localStorage.getItem('refresh_token');
  try {
    if (!refreshToken) {
      router.push({ path: '/' });
      return;
    }
    const response = await axios.post(
      routesContainer.REFRESH_USER_TOKEN,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`
        }
      }
    );

    if (response.status === 200) {
      const accessToken = response.data.content[0].access_token;
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

async function getUserInformation() {
  try {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.get(routesContainer.GET_USER_INFORMATION, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    console.log('Full response:', response);  

    if (response.data && response.data.content && Array.isArray(response.data.content) && response.data.content.length > 0) {
      return response.data.content[0];  
    } else {
      console.error('Unexpected response structure:', response.data);
      return null;
    }
  } catch (error) {
    console.error('Error fetching user information:', error);
    if (error.response) {
      console.error('Error response:', error.response.data);
    }
    return null;
  }
}

async function isUserVerified() {
  try {
    const response = await getUserInformation();
    const verification = response.verification;
    return verification === 'done';
  } catch (error) {
    console.error(error);
    return false;
  }
}

async function isUserExisting() {
  try {
    const email = await getEmailByToken();
    const response = await axios.post(routesContainer.EXISTS_USER, { email: email });
    const exists = response.data.content[0].exists as boolean;
    return exists;
  } catch (error) {
    console.error(error);
    return false;
  }
}

async function hasAuthRejection() {
  try {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.get(routesContainer.HAS_AUTH_REJECTION, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    console.log(response);

    if (response.data && response.data.content[0] && response.data.content[0].length > 0) {
      const hasRejection = response.data.content[0].has_rejection as boolean;
      return hasRejection;
    } else {
      console.error("Unexpected response structure", response);
      return false;
    }
  } catch (error: any) {
    if (error.response && error.response.status === 401) {
      return false;
    }
    return false;
  }
}

export { getEmailByToken, checkAuth, getUserInformation, isUserVerified, isUserExisting, hasAuthRejection, checkAuthRejection, tryRefreshToken };
