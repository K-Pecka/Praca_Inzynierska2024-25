import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import homeRoutes from "./homeRoutes";
import panelRoutes from "./panelRoutes";
import authRoutes from "./authRoutes";
import { useUserStore, useMessageStore } from "@/stores";

const routes: RouteRecordRaw[] = [authRoutes, homeRoutes, panelRoutes];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const siteName = import.meta.env.VITE_APP_SITE_TITLE;
  document.title = to.meta.title ? `${siteName} - ${to.meta.title}` : siteName;

  const { isLogin } = useUserStore();
  const { setErrorCurrentMessage } = useMessageStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const goBack = to.matched.some((record) => record.meta.goBack);

  if (requiresAuth && !(await isLogin())) {
    setErrorCurrentMessage('Wymagana jest autoryzacja. Proszę się zalogować.');
    next({ name: 'logIn' });
  } else if (goBack && (await isLogin())) {
    next(from.name ? { name: from.name } : { name: "landing" });
  } else {
    next();
  }
});

export default router;
