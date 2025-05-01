import type { RouteRecordRaw } from "vue-router";
import { LogOut, LogIn, Register } from "@/views/auth";
import { Home } from "@/views/home";

const authRoutes: RouteRecordRaw[] = [
  {
    path: "/auth",
    name: "auth",
    component: Home,
    meta: { title: "Home" },
  },
  {
    path: "/auth/log-out",
    name: "logOut",
    component: LogOut,
  },
];

export default authRoutes;
