import { createWebHistory } from 'vue-router';
import Dashboard from "@/layouts/PanelLayout.vue";


const tripRoutes = {
  path: "/dashboard/:tripId",
  name: "Dashboard",
  history: createWebHistory(import.meta.env.BASE_URL),
  component: Dashboard,
  meta: {requiresAuth: true},
};

export default tripRoutes;