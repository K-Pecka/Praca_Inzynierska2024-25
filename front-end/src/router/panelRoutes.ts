import type { RouteRecordRaw } from "vue-router";

import {
  YourItinerary, ExpenseTracker, TicketsView, ParticipantsView, TripEditForm,
  PlanForm, TripDashboard, YourTrip, ActivityView,DebtView
} from "@/views/panel";

import PanelLayout from "@/layouts/PanelLayout.vue";

const panelRoutes: RouteRecordRaw = {
  path: "/:role/panel/:tripId",
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
      path: "itineraries",
      name: "itineraries",
      component: YourItinerary
    },
    {
      path: "itineraries/create",
      name: "createItinerary",
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
      path: "debt",
      name: "debt",
      component: DebtView
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
      path: "plan/:itineraryId/activity",
      name: "ActivityView",
      component: ActivityView
    },
  ]
}


export default panelRoutes;