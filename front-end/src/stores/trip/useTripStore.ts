import { defineStore } from "pinia";
import { useParticipants } from "./useParticipants";
import { useDashboard } from "./useDashboard";
import { usePlans } from "./usePlans";
import { useTrips } from "./useTrips";
import { useBudget } from "./useBudget";
import { useActivity } from "./useActivity";
import { useTicket } from "./useTicket";
import { useUtilsStore } from "@/stores";
export const useTripStore = defineStore("trip", () => {
  const { getTripId, getPlanId } = useUtilsStore();

  const { getDashboard, getSpecialSectionName } = useDashboard(getTripId);
  const { getTrips, getTripDetails, deleteTrip, createTrip, updateTrip } =
    useTrips(getTripId);
  const { tripMutationBudget, createExpense, getExpensByTrip } =
    useBudget(getTripId);
  const { getPlans, addPlan, getPlanDetails, planBtn } = usePlans(
    getTripId,
    getPlanId
  );

  const { getActivities } = useActivity(getTripId, getPlanId);

  const { deleteTicket, createTicket, getTickets } = useTicket(getTripId);

  const { addParticipant, removeParticipant } = useParticipants();

  return {
    dashboard: {
      getDashboard,
      getSpecialSectionName,
    },
    budget: {
      getExpensByTrip,
    },
    trip: {
      getTrips,
      getTripDetails,
      deleteTrip,
      createTrip,
      updateTrip,
    },
    plan: { getPlans, addPlan, planBtn, getPlanDetails },
    activity: { getActivities },
    ticket: { deleteTicket, createTicket, getTickets },
    tripMutationBudget,
    removeParticipant,
    addParticipant,
    getTickets,
    createExpense,
  };
});
// import { useParticipants } from "./useParticipants";
// import { useDashboard } from "./useDashboard";
// import { usePlans } from "./usePlans";
// import { useTrips } from "./useTrips";
// import { useBudget } from "./useBudget";
// import { useTicketStore } from "@/stores";

// export const useTripStore = defineStore("trip", () => {
//   // Dashboard
//   const { getDashboard, getExpenseItem } = useDashboard();

//   // Plans
//   const { getPlans, yourPlans, addPlan } = usePlans();

//   // Trips
//   const { yourTrips, getTripDetails, getTrips, addTrip, updateTrip } = useTrips();

//   // Participants
//   const { addParticipant, removeParticipant } = useParticipants();

//   // Budget
//   const { addExpense, getExpenses, budgetMutation } = useBudget();

//   // Tickets
//   const { getTickets } = useTicketStore();

//   return {
//     dashboard: {
//       getDashboard,
//       getExpenseItem,
//     },
//     plans: {
//       getPlans,
//       yourPlans,
//       addPlan,
//     },
//     trips: {
//       yourTrips,
//       getTripDetails,
//       getTrips,
//       addTrip,
//       updateTrip,
//     },
//     participants: {
//       addParticipant,
//       removeParticipant,
//     },
//     budget: {
//       addExpense,
//       getExpenses,
//       budgetMutation,
//     },
//     tickets: {
//       getTickets,
//     },
//   };
// });
