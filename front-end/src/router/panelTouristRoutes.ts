import type { RouteRecordRaw } from "vue-router";

import {
  YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm,
  PlanForm, BudgetForm, TripDashboard, YourTrip, ActivityView
} from "@/views/panel";

import PanelLayout from "@/layouts/PanelLayout.vue";

const panelRoutes: RouteRecordRaw = {
  path: "/panel/:tripId",
  component: PanelLayout,
  name: "panel",
  meta: { title: "Panel", requiresAuth: true },
  props: true,
  children: [
    {
      path: "",
      name: "tripDashboard",
      component: TripDashboard
    },
    {
      path: "plans",
      name: "tripPlans",
      component: YourPlan
    },
    {
      path: "plans/create",
      name: "createPlan",
      component: PlanForm
    },
    {
      path: "tickets",
      name: "yourTickets",
      component: TicketsView
    },
    {
      path: "budgets",
      name: "ExpenseTracker",
      component: ExpenseTracker
    },
    {
      path: "budgets/edit",
      name: "editBudget",
      component: BudgetForm
    },
    {
      path: "participants",
      name: "tripParticipants",
      component: ParticipantsView
    },
    {
      path: "edit",
      name: "editTrip",
      component: TripEditForm
    },
    {
      path: "trip",
      name: "yourTrip",
      component: YourTrip
    },
    {
      path: "plan/:planId/activity",
      name: "ActivityView",
      component: ActivityView
    },
  ]
}


export default panelRoutes;