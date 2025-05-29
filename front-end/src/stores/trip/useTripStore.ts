import { defineStore } from "pinia";
import { useParticipants } from "./useParticipants";
import { useDashboard } from "./useDashboard";
import { usePlans } from "./usePlans";
import { useTrips } from "./useTrips";
import { useBudget } from "./useBudget";
import {useDebt} from './useDebt'
import { useTicketStore, useUtilsStore } from "@/stores";
export const useTripStore = defineStore("trip", () => {
  const { getTripId } = useUtilsStore();
  
  const { getDashboard, getSpecialSectionName } = useDashboard(getTripId);
  const {
    getTrips,
    getTripDetails,
    deleteTrip,
    createTrip,
    updateTrip,
    updateTripBudget
  } = useTrips(getTripId);
  const {createExpense, getExpenseByTrip,deleteExpense,setFilters,getFilters } =
    useBudget(getTripId);

  const {createDebt,getDebt,removeMember,deleteDebt} = useDebt(getTripId)
  const { getPlans, yourPlans, planMutationAdd, handleDeleteItinerary } = usePlans(getTripId);

  const { addParticipant, removeParticipant } = useParticipants();

  const { getTickets,createTicket,deleteTicket,updateMembers } = useTicketStore();
  return {
    dashboard: {
      getDashboard,
      getSpecialSectionName,
    },
    budget: {
      getExpensByTrip: getExpenseByTrip,
      deleteExpense,
      createExpense,
      setFilters,
      getFilters
    },
    debt:{
      createDebt,
      getDebt,
      removeMember,
      deleteDebt
    },
    trip:{
      getTrips,
      getTripDetails,
      deleteTrip,
      createTrip,
      updateTrip,
      updateTripBudget
    },
    plan:{
      handleDeleteItinerary
    },
    ticket:{
      getTickets,
      createTicket,
      deleteTicket,
      updateMembers
    },
    yourPlans,
    getPlans,
    getTripDetails,
    planMutationAdd,
    removeParticipant,
    addParticipant,
  };
});