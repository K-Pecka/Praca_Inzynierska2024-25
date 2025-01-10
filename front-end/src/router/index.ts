import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Home from '@/views/Home.vue';
import Landing from '@/views/children/Landing.vue';
import LogIn from '@/views/children/LogIn.vue';
import Register from '@/views/children/Register.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Home' },
    children: [
      {
        path: '',
        name: 'landing',
        component: Landing,
      },
      {
        path: 'logIn',
        name: 'logIn',
        component: LogIn,
      },
      {
        path: 'register',
        name: 'register',
        component: Register,
      },
    ],
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const siteName = import.meta.env.VITE_APP_SITE_NAME;
  document.title = to.meta.title ? `${to.meta.title} - ${siteName}` : siteName;
  next();
});
export default router;
