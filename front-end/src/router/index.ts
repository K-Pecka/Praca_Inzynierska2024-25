import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router'; 
import Home from '@/views/Home.vue';
import Landing from '@/views/children/Landing.vue';
import LogIn from '@/views/children/LogIn.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
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
    ],
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;