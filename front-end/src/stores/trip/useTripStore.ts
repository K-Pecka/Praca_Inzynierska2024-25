import {defineStore} from "pinia";
import {useParticipants} from "./useParticipants";
import {useDashboard} from "./useDashboard";
import {usePlans} from "./usePlans";
import {useTrips} from "./useTrips";
import { useBudget } from "./useBudget";
import { useTicketStore } from "./useTicketStore";
export const useTripStore = defineStore("trip", () => {

  const { getDashboard, getExpenseItem } = useDashboard();
  const { getPlans, yourPlans, planMutationAdd } = usePlans();
  const { yourTrips, getTripDetails, getTrips, tripMutationAdd, tripMutationUpdate } = useTrips();
  const { addParticipant, removeParticipant } = useParticipants();
  const { tripMutationBudget,getExpensesQuery } = useBudget();
  const { getTickets } = useTicketStore();
  return {
    getExpenseItem,
    getPlans,
    getDashboard,
    yourTrips,
    yourPlans,
    getTripDetails,
    getTrips,
    tripMutationAdd,
    tripMutationBudget,
    getExpensesQuery,
    planMutationAdd,
    tripMutationUpdate,
    removeParticipant,
    addParticipant,
    getTickets
  };
});
