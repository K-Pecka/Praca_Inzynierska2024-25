import type { RouteRecordRaw } from "vue-router";
import { Home, Landing, PricingSection } from "@/views/home";
import { Error_500,Error_404 } from "@/views/unexpected";

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
        path: "/pricing-section",
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
  {
    path: "/404",
    name: "error_404",
    component: Error_404,
  },
  {
    path: '/:pathMatch(.*)*',
    component: Error_404,
  }
];

export default homeRoutes;
