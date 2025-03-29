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

    { path: "your-trip", name: "yourTrip", component: YourTrip },
    { path: "your-trip/:tripId", name: "tripDashboard", component: TripDashboard },
    { path: "your-trip/:tripId/your-plan", name: "yourPlan", component: YourPlan },
    { path: "your-trip/:tripId/tickets-view", name: "TicketsView", component: TicketsView },
    { path: "your-trip/:tripId/expense-tracker", name: "ExpenseTracker", component: ExpenseTracker },
    { path: "your-trip/:tripId/participants-view", name: "ParticipantsView", component: ParticipantsView },
    { path: "your-trip/:tripId/trip-edit", name: "TripEdit", component: TripEditForm },

    { path: "your-trip/trip", name: "TripForm", component: TripForm },
    { path: "your-trip/:tripId/plan-form", name: "PlanForm", component: PlanForm },
    { path: "your-trip/:tripId/budget", name: "budget", component: BugdetForm },
  ],
};


export default panelRoutes;
