import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import homeRoutes from "./homeRoutes";
import panelRoutes from "./panelRoutes";
import tripRoutes from "@/router/tripRoutes";
import inviteRouters from "./inviteRouters"
import infotRoutes from "./infotRoutes"
import { useAuthStore, useNotificationStore } from "@/stores";

const routes: RouteRecordRaw[] = [
  ...homeRoutes,
  panelRoutes,
  tripRoutes,
  inviteRouters,
  infotRoutes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach(async (to, from, next) => {
  const currentPath = typeof to.name === "string" ? to.name : "landing";
  const siteName = import.meta.env.VITE_APP_SITE_TITLE;
  document.title = to.meta.title ? `${siteName} - ${to.meta.title}` : siteName;

  const auth = useAuthStore();
  const { setErrorCurrentMessage } = useNotificationStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const goBack = to.matched.some((record) => record.meta.goBack);
  const routerName = typeof to.name === "string" ? to.name : undefined;

  const token = auth.getToken();

  if (goBack && token?.access) {
    setErrorCurrentMessage("Przed wejściem na tą stronę wyloguj się.");
    return next(from.name ? { name: from.name } : { name: "landing" });
  }

  if (token?.access) {
    const allowed = await auth.checkPermission(routerName, "path");
    if (!allowed) {
      setErrorCurrentMessage("Brak dostępu do tej zawartości");
      const lastVisitedRoute = localStorage.getItem("routerPath");

      if (Object.keys(to.params).length > 0) {
        return next(
            lastVisitedRoute
                ? { name: lastVisitedRoute, params: { ...from.params } }
                : { name: "landing" }
        );
      } else {
        return next(lastVisitedRoute ? { name: lastVisitedRoute } : { name: "landing" });
      }
    }
  }

  localStorage.setItem("routerPath", currentPath);
  next();
});


export default router;
