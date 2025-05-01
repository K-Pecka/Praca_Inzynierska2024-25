import type { RouteRecordRaw } from "vue-router";

import {
  YourPlan, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm,
  PlanForm, BudgetForm, TripDashboard, YourTrip
} from "@/views/panel";

import Dashboard from "@/layouts/PanelLayout.vue";

const panelRoutes: RouteRecordRaw = {
  path: "/panel",
  component: Dashboard,
  meta: { title: "Panel", requiresAuth: true },
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
    }
  ]
}


export default panelRoutes;