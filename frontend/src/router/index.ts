import { createRouter, createWebHistory } from 'vue-router';
import AuthView from '../views/AuthView.vue';
import DashboardView from '../views/DashboardView.vue';
import SettingsView from '../views/SettingsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/auth/:code?',
      name: 'auth',
      component: AuthView,
      props: (route) => ({ code: route.params.code })
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    }
  ]
});

export default router;
