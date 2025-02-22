import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import homeRoutes from "./homeRoutes";
import panelRoutes from "./panelRoutes";
import authRoutes from "./authRoutes";
import { useAuthStore, useNotificationStore } from "@/stores";

const routes: RouteRecordRaw[] = [...authRoutes, homeRoutes, panelRoutes];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const siteName = import.meta.env.VITE_APP_SITE_TITLE;
  document.title = to.meta.title ? `${siteName} - ${to.meta.title}` : siteName;

  const { validToken } = useAuthStore();
  const { setErrorCurrentMessage } = useNotificationStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const goBack = to.matched.some((record) => record.meta.goBack);
  if (requiresAuth && !(await validToken())) {
    setErrorCurrentMessage('Wymagana jest autoryzacja.\n Proszę się zalogować.');
    next({ name: 'logIn' });
  } else if (goBack && (await validToken())) {
    setErrorCurrentMessage('Przed wejściem na tą stronę wyloguj się.');
    next(from.name ? { name: from.name } : { name: "landing" });

  } else {
    next();
  }
});

export default router;
