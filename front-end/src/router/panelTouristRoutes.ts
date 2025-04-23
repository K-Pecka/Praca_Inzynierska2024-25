import type { RouteRecordRaw } from "vue-router";

import { 
  Panel, RoleSelection, TripDashboard, YourTrip, YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm, ActivityView,
  PlanForm, TripForm, BudgetForm
} from "@/views/panel";
import { AccountSettings } from "@/views/account";
import { Role } from "@/types/enum";

const panelRoutes: RouteRecordRaw = {
  path: "/panel",
  name: "panel",
  component: Panel,
  meta: { title: "Panel", requiresAuth: true },
  children: [
    { path: "", name: "roleSelection", component: RoleSelection },
    { path: "account-settings", name: "AccountSettings", component: AccountSettings },

    { path: "trips", name: "yourTrip", component: YourTrip },
    { path: "trip/:tripId", name: "tripDashboard", component: TripDashboard },
    { path: "trip/:tripId/plan", name: "yourPlan", component: YourPlan },
    { path: "trip/:tripId/tickets-view", name: "TicketsView", component: TicketsView },
    { path: "trip/:tripId/expense-tracker", name: "ExpenseTracker", component: ExpenseTracker },
    { path: "trip/:tripId/participants-view", name: "ParticipantsView", component: ParticipantsView },
    { path: "trip/:tripId/trip-edit", name: "TripEdit", component: TripEditForm },
    { path: "trip/:tripId/plan/:planId/activity", name: "ActivityView", component: ActivityView },

    { path: "trip/trip", name: "TripForm", component: TripForm },
    { path: "trip/:tripId/plan-form", name: "PlanForm", component: PlanForm },
    { path: "trip/:tripId/budget", name: "budget", component: BudgetForm },
  ],
};


export default panelRoutes;
