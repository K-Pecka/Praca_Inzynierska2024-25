<<<<<<< Updated upstream
import { defineStore } from "pinia";
import { useParticipants } from "./useParticipants";
import { useDashboard } from "./useDashboard";
import { usePlans } from "./usePlans";
import { useTrips } from "./useTrips";
import { useBudget } from "./useBudget";
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
  } = useTrips(getTripId);
  const { tripMutationBudget, createExpense, getExpensByTrip } =
    useBudget(getTripId);
  const { getPlans, yourPlans, planMutationAdd, handleDeleteItinerary } = usePlans(getTripId);
=======
import {useMutation, useQueryClient} from "@tanstack/vue-query";
import {fetchAddParticipant, fetchRemoveParticipant} from "@/api";
import {useNotificationStore} from "@/stores";
>>>>>>> Stashed changes

export const useTripStore = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();

<<<<<<< Updated upstream
  const { getTickets } = useTicketStore();
  return {
    dashboard: {
      getDashboard,
      getSpecialSectionName,
    },
    budget: {
      getExpensByTrip,
    },
    trip:{
      getTrips,
      getTripDetails,
      deleteTrip,
      createTrip,
      updateTrip
    },
    plan:{
      handleDeleteItinerary
    },
    yourPlans,
    getPlans,
    getTripDetails,
    tripMutationBudget,
    planMutationAdd,
    removeParticipant,
    addParticipant,
    getTickets,
    createExpense,
  };
});
// import { defineStore } from "pinia";
// import { useParticipants } from "./useParticipants";
// import { useDashboard } from "./useDashboard";
// import { usePlans } from "./usePlans";
// import { useTrips } from "./useTrips";
// import { useBudget } from "./useBudget";
// import { useTicketStore } from "@/stores";
=======
    const addParticipantMutation = useMutation({
        mutationFn: ({idTrip, participant}: {
            idTrip: number, participant: { name: string, email: string }
        }) => fetchAddParticipant(idTrip, participant),
        onSuccess: (idTrip) => {
            notifications.setSuccessCurrentMessage("Dodano uczestnika");
            queryClient.invalidateQueries({queryKey: ["trip", String(idTrip)]});
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(err.message || "Błąd"),
    });
>>>>>>> Stashed changes

    const removeParticipantMutation = useMutation({
        mutationFn: ({idTrip, idParticipant}: {
            idTrip: number; idParticipant: number;
        }) => fetchRemoveParticipant(idTrip, idParticipant),
        onSuccess: (idTrip) => {
            notifications.setSuccessCurrentMessage("Usunięto uczestnika");
            queryClient.invalidateQueries({queryKey: ["trip", String(idTrip)]});
        },
        onError: (err: any) =>
            notifications.setErrorCurrentMessage(err.message || "Błąd"),
    });

    const addParticipant = (
        idTrip: number,
        participant: { name: string; email: string }
    ) => addParticipantMutation.mutateAsync({idTrip, participant});

    const removeParticipant = (idTrip: number, idParticipant: number) =>
        removeParticipantMutation.mutateAsync({idTrip, idParticipant});

    return {addParticipant, removeParticipant};
};
