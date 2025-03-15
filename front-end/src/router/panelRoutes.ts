import type { RouteRecordRaw } from "vue-router";

import { 
  Panel, RoleSelection, TripDashboard, YourTrip, YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm
} from "@/views/panel";

import { PlanForm, TripForm, BugdetForm } from "@/views/panel/children/form";

const panelRoutes: RouteRecordRaw = {
  path: "/panel",
  name: "panel",
  component: Panel,
  meta: { title: "Panel", requiresAuth: true },
  children: [
    { path: "", name: "roleSelection", component: RoleSelection },

    { path: "yourTrip", name: "yourTrip", component: YourTrip },
    { path: "yourTrip/:tripId", name: "tripDashboard", component: TripDashboard },
    { path: "yourTrip/:tripId/yourPlan", name: "yourPlan", component: YourPlan },
    { path: "yourTrip/:tripId/TicketsView", name: "TicketsView", component: TicketsView },
    { path: "yourTrip/:tripId/expenseTracker", name: "ExpenseTracker", component: ExpenseTracker },
    { path: "yourTrip/:tripId/participantsView", name: "ParticipantsView", component: ParticipantsView },
    { path: "yourTrip/:tripId/tripEdit", name: "TripEdit", component: TripEditForm },

    { path: "tripForm", name: "TripForm", component: TripForm },
    { path: "yourTrip/:tripId/planForm", name: "PlanForm", component: PlanForm },
    { path: "yourTrip/:tripId/budget", name: "budget", component: BugdetForm },
  ],
};

export default panelRoutes;
