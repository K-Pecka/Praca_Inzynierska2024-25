import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import homeRoutes from "./homeRoutes";
import panelRoutes from "./panelTouristRoutes";
import tripRoutes  from "@/router/tripRoutes";
import panelGuideRoutes from "./panelGuideRoutes";
import authRoutes from "./authRoutes";
import { useAuthStore, useNotificationStore } from "@/stores";

const routes: RouteRecordRaw[] = [...authRoutes, ...homeRoutes, panelRoutes, panelGuideRoutes, tripRoutes];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const currentPath = typeof to.name === "string" ? to.name : "landing";
  const siteName = import.meta.env.VITE_APP_SITE_TITLE;
  document.title = to.meta.title ? `${siteName} - ${to.meta.title}` : siteName;

  const { validToken, checkPermission } = useAuthStore();
  const { setErrorCurrentMessage } = useNotificationStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const goBack = to.matched.some((record) => record.meta.goBack);

  const routerName = typeof to.name === "string" ? to.name : undefined;
  if (requiresAuth && !(await validToken())) {
    setErrorCurrentMessage(
      "Tylko zalogowani użytkownicy,\n posiadają dostępn do tej zawartości."
    );
    next({ name: "logIn" });
  } else if (goBack && (await validToken())) {
    setErrorCurrentMessage("Przed wejściem na tą stronę wyloguj się.");
    next(from.name ? { name: from.name } : { name: "landing" });
  } else if (!(await checkPermission(routerName, "path"))) {
    setErrorCurrentMessage("Brak dostępu do tej zawartości");
    const lastVisitedRoute = localStorage.getItem("routerPath");
    if (Object.keys(to.params).length > 0) {
      next(
        lastVisitedRoute
          ? { name: lastVisitedRoute, params: { ...from.params } }
          : { name: "landing" }
      );
    } else {
      next(lastVisitedRoute ? { name: lastVisitedRoute } : { name: "landing" });
    }
    return;
  } else {
    localStorage.setItem("routerPath", currentPath);
    next();
  }
});

export default router;
