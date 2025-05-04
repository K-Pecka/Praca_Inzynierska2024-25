import type { RouteRecordRaw } from "vue-router";

import { 
  TripDashboard, YourTrip, YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm, ActivityView,
  PlanForm, TripForm, BudgetForm
} from "@/views/panel";
import PanelLayout from "@/layouts/PanelLayout.vue";

const panelGuideRoutes: RouteRecordRaw = {
  path: "/guide",
  name: "panelGuide",
  component: PanelLayout,
  meta: { title: "Panel", requiresAuth: true },
  children: [

    { path: "trips", name: "yourTripGuide", component: YourTrip },
    { path: "trip/:tripId", name: "tripDashboardGuide", component: TripDashboard },
    { path: "trip/:tripId/plan", name: "yourPlanGuide", component: YourPlan },
    { path: "trip/:tripId/tickets-view", name: "TicketsViewGuide", component: TicketsView },
    { path: "trip/:tripId/expense-tracker", name: "ExpenseTrackerGuide", component: ExpenseTracker },
    { path: "trip/:tripId/participants-view", name: "ParticipantsViewGuide", component: ParticipantsView },
    { path: "trip/:tripId/trip-edit", name: "TripEditGuide", component: TripEditForm },
    { path: "trip/:tripId/plan/:planId/activity", name: "ActivityViewGuide", component: ActivityView },

    { path: "trip/trip", name: "TripFormGuide", component: TripForm },
    { path: "trip/:tripId/plan-form", name: "PlanFormGuide", component: PlanForm },
    { path: "trip/:tripId/budget", name: "budgetGuide", component: BudgetForm },
  ],
};


export default panelGuideRoutes;
