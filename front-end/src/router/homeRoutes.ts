import type { RouteRecordRaw } from "vue-router";
import { Home, Landing, PricingSection } from "@/views/home";

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
      path: "/pricingSection",
      name: "pricingSection",
      component: PricingSection,
    }
  ],
};

export default homeRoutes;
