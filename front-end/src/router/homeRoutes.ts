import type { RouteRecordRaw } from "vue-router";
import { Home, Landing, PricingSection } from "@/views/home";
import { Error_500 } from "@/views/unexpected";

const homeRoutes: RouteRecordRaw[] = [
  {
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
      },
    ],
  },
  {
    path: "/500",
    name: "error_500",
    component: Error_500,
  },
];

export default homeRoutes;
