import { createRouter, createWebHistory } from 'vue-router';

import {
  TripDashboard
} from "@/views/panel";

const tripRoutes = {
  path: "/dashboard/:tripId",
  name: "tripDashboard",
  history: createWebHistory(import.meta.env.BASE_URL),
  component: TripDashboard,
  meta: {requiresAuth: true},
};

export default tripRoutes;