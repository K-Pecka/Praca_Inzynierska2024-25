import type { RouteRecordRaw } from "vue-router";
import { LogOut } from "@/views/logOut";

const authRoutes: RouteRecordRaw = {
  path: "/logOut",
  name: "logOut",
  component: LogOut,
};

export default authRoutes;
