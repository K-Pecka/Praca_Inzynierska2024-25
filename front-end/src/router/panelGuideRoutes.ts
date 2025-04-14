import type { RouteRecordRaw } from "vue-router";

import { 
  Panel, TripDashboard, YourTrip, YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm, ActivityView,
  PlanForm, TripForm, BudgetForm
} from "@/views/panel";

const panelGuideRoutes: RouteRecordRaw = {
  path: "/guide",
  name: "panelGuide",
  component: Panel,
  meta: { title: "Panel", requiresAuth: true },
  children: [

    { path: "your-trip", name: "yourTripGuide", component: YourTrip },
    { path: "your-trip/:tripId", name: "tripDashboardGuide", component: TripDashboard },
    { path: "your-trip/:tripId/your-plan", name: "yourPlanGuide", component: YourPlan },
    { path: "your-trip/:tripId/tickets-view", name: "TicketsViewGuide", component: TicketsView },
    { path: "your-trip/:tripId/expense-tracker", name: "ExpenseTrackerGuide", component: ExpenseTracker },
    { path: "your-trip/:tripId/participants-view", name: "ParticipantsViewGuide", component: ParticipantsView },
    { path: "your-trip/:tripId/trip-edit", name: "TripEditGuide", component: TripEditForm },
    { path: "your-trip/:tripId/your-plan/:planId/activity", name: "ActivityViewGuide", component: ActivityView },

    { path: "your-trip/trip", name: "TripFormGuide", component: TripForm },
    { path: "your-trip/:tripId/plan-form", name: "PlanFormGuide", component: PlanForm },
    { path: "your-trip/:tripId/budget", name: "budgetGuide", component: BudgetForm },
  ],
};


export default panelGuideRoutes;
