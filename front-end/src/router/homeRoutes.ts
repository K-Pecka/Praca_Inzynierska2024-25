import type { RouteRecordRaw } from "vue-router";
import Home from "@/layouts/HomeLayout.vue";
import { Landing, PricingSection, ContactUs } from "@/views/home";
import { AccountSettings } from "@/views/account";
import { Error_500,Error_404 } from "@/views/unexpected";
import {LogIn, Register,LogOut} from "@/views";

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
      {
        path: "/about-us",
        name: "aboutUs",
        component: () => import("@/views/home/AboutUs.vue"),
      },
      {
        path: "/contact-us",
        name: "contactUs",
        component: ContactUs,
      },
      {
        path: "login",
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
      {
        path: "logOut",
        name: "logOut",
        component: LogOut,
      },
      {
        path: "settings",
        name: "AccountSettings",
        component: AccountSettings
      }
    ]
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
