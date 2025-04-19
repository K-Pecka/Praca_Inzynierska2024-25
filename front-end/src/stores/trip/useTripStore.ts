import {defineStore} from "pinia";
import {useParticipants} from "./useParticipants";
import {useDashboard} from "./useDashboard";
import {usePlans} from "./usePlans";
import {useTrips} from "./useTrips";
import {useTripMutations} from "./useTripMutations";

export const useTripStore = defineStore("trip", () => {

  const { getDashboard, getExpenseItem } = useDashboard();
  const { getPlans, yourPlans, planMutationAdd } = usePlans();
  const { yourTrips, getTripDetails, getTrips } = useTrips();
  const { tripMutationAdd, tripMutationUpdate, tripMutationBudget } = useTripMutations();
  const { addParticipant, removeParticipant } = useParticipants();

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
    planMutationAdd,
    tripMutationUpdate,
    removeParticipant,
    addParticipant,
  };
});
