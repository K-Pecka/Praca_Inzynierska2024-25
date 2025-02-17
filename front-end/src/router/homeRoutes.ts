import type { RouteRecordRaw } from "vue-router";
import { Home, Landing } from "@/views/home";

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
    }
  ],
};

export default homeRoutes;
