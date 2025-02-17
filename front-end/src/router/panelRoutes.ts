import type { RouteRecordRaw } from "vue-router";
import { 
  Panel, RoleSelection, TripDashboard, YourTrip, YourPlan, ExpenseTracker,
  PlanForm, TripForm, BugdetForm
} from "@/views/panel";

const panelRoutes: RouteRecordRaw = {
  path: "/panel",
  name: "panel",
  component: Panel,
  meta: { title: "Panel", requiresAuth: true },
  children: [
    {
      path: "",
      name: "roleSelection",
      component: RoleSelection,
    },
    {
      path: "yourTrip",
      name: "yourTrip",
      component: YourTrip,
    },
    {
      path: "yourTrip/:tripId",
      name: "tripDashboard",
      component: TripDashboard,
    },
    {
      path: "yourTrip/:tripId/yourPlan",
      name: "yourPlan",
      component: YourPlan,
    },
    {
      path: ":tripId/planForm",
      name: "PlanForm",
      component: PlanForm,
    },
    {
      path: "tripForm",
      name: "TripForm",
      component: TripForm,
    },
    {
      path: ":tripId/expenseTracker",
      name: "ExpenseTracker",
      component: ExpenseTracker,
    },
    {
      path: ":tripId/budget",
      name: "budget",
      component: BugdetForm,
    },
  ],
};

export default panelRoutes;
