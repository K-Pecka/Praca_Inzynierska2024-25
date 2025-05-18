import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import homeRoutes from "./homeRoutes";
import panelRoutes from "./panelRoutes";
import tripRoutes from "@/router/tripRoutes";
import authRoutes from "./authRoutes";
import inviteRouters from "./inviteRouters"
import { useAuthStore, useNotificationStore } from "@/stores";
import { useRoleStore } from "@/stores/auth/useRoleStore";

import { useQueryClient } from "@tanstack/vue-query";
import { tripsQueryReload } from "@/api/services/tripQuery";
import { fetchUserRole } from "@/api/endpoints/auth";
const routes: RouteRecordRaw[] = [
  ...authRoutes,
  ...homeRoutes,
  panelRoutes,
  tripRoutes,
  inviteRouters
];

const router = createRouter({
  history: createWebHistory(),
  routes,
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

  if (requiresAuth && !(await auth.validToken())) {
    setErrorCurrentMessage("Tylko zalogowani użytkownicy,\n posiadają dostęp do tej zawartości.");
    return next({ name: "logIn" });
  }

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

router.beforeEach(async (to, from, next) => {
  const roleParam = to.params.role as string | undefined;
  const roleStore = useRoleStore();
  const queryClient = useQueryClient();

  if (!roleParam) return next();
  if (roleParam === roleStore.getRole()) return next();

  try {
    await fetchUserRole(roleParam);
    roleStore.setRole(roleParam);

    await queryClient.removeQueries({ queryKey: ['trips'] });
    await queryClient.fetchQuery(tripsQueryReload());

    next();
  } catch (err) {
    console.error('Błąd przy zmianie roli w beforeEach', err);
    next('/unauthorized');
  }
});


export default router;
