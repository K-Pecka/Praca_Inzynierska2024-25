import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import Home from "@/views/home/Home.vue";
import Panel from "@/views/panel/Panel.vue";
import Landing from "@/views/home/children/Landing.vue";
import LogIn from "@/views/home/children/LogIn.vue";
import Register from "@/views/home/children/Register.vue";
import RoleSelection from "@/views/panel/children/RoleSelection.vue";
import LogOut from "@/views/logOut/LogOut.vue";
import Trip from "@/views/panel/children/Trip.vue";

import { useUserStore } from "@/stores/userStore";
import { useMessageStore } from "@/stores/messageStore";
const routes: RouteRecordRaw[] = [
  {
    path:"/logOut",
    name:"logOut",
    component:LogOut,
  },
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { title: "Home" },
    children: [
      {
        path: "",
        name: "landing",
        component: Landing,
      },
      {
        path: "logIn",
        name: "logIn",
        component: LogIn,
        meta: { goBack: true },
      },
      {
        path: "register",
        name: "register",
        component: Register,
        meta: { goBack: true },
      },
    ],
  },
  {
    path: "/panel",
    name: "panel",
    component: Panel,
    meta: { title: "Panel", requiresAuth: true },
    children: [
      {
        path: "",
        name: "roleSelection",
        component: RoleSelection,
      },
      {
        path: "trip",
        name: "trip",
        component: Trip,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const siteName = import.meta.env.VITE_APP_SITE_TITLE;
  document.title = to.meta.title ? `${to.meta.title} - ${siteName}` : siteName;

  const { isLogin } = useUserStore();
  const { setErrorCurrentMessage } = useMessageStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const goBack = to.matched.some((record) => record.meta.goBack);

  if (requiresAuth && !(await isLogin())) {
    setErrorCurrentMessage('Wymagana jest autoryzacja. Proszę się zalogować.')
    next({name: 'logIn'});
  } else if (goBack && (await isLogin())) {
    next(from.name ? { name: from.name } : { name: "landing" });
  } else {
    next();
  }
});

export default router;
