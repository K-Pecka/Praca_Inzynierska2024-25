import type { RouteRecordRaw } from "vue-router";
import { LogOut, LogIn, Register } from "@/views/auth";
import { Home } from "@/views/home";

const homeRoutes: RouteRecordRaw[] = [
  {
    path: "/auth",
    name: "auth",
    component: Home,
    meta: { title: "Home" },
    children: [
      {
        path: "",
        name: "logIn",
        component: LogIn,
        meta: { goBack: true, title: "Logowanie" },
      },
      {
        path: "register",
        name: "register",
        component: Register,
        meta: { goBack: true, title: "Rejestracja" },
      }
    ],
  },
  {
    path: "/auth/logOut",
    name: "logOut",
    component: LogOut,
  },
];

export default homeRoutes;
