import type { RouteRecordRaw } from "vue-router";
import { Home, Landing, LogIn, Register } from "@/views/home";

const homeRoutes: RouteRecordRaw = {
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
      meta: { goBack: true, title: "Logowanie" },
    },
    {
      path: "register",
      name: "register",
      component: Register,
      meta: { goBack: true, title: "Rejestracja" },
    },
  ],
};

export default homeRoutes;
