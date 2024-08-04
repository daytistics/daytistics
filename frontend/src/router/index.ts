import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/auth/:code?',
      name: 'auth',
      component: () => import('../views/AuthView.vue'),
      props: (route) => ({ code: route.params.code })
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue')
    },
    {
      path: '/auth/rejected',
      name: 'authRejected',
      component: () => import('../views/AuthRejectedView.vue')
    }
  ]
});

export default router;
