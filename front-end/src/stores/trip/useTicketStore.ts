import { defineStore } from "pinia";
import {
  getTicketsQuery,
  createTicketMutation,
  getMutationDelete,
  getMutationUpdate
} from "@/api/services/ticketQuery";
import { useUtilsStore } from "../utils/useUtilsStore";
import { useNotificationStore } from "../ui/useNotificationStore";
import { useQueryClient } from "@tanstack/vue-query";

export const useTicketStore = defineStore("ticket", () => {
  const { getTripId } = useUtilsStore();
  const queryClient = useQueryClient();
  const notifications = useNotificationStore();

  const createTicket = createTicketMutation({
    tripId: getTripId,
    notifications,
    queryClient,
    successMessage: "Dodano poyślnie bilet",
    errorMessage: "Nie udało się dodać biletu",
  });
  const deleteTicket = getMutationDelete({
    tripId: getTripId,
    notifications,
    queryClient,
    successMessage: "Usunięto pomyślnie bilet",
    errorMessage: "Nie udało się usunąć biletu",
  })
  const updateMembers = getMutationUpdate({
    tripId: getTripId,
    notifications,
    queryClient,
    successMessage: "Dostęp do biletu został zminiony",
    errorMessage: "Nie udało się zmienić dostępu biletu",
  })
  const getTickets = (tripId?: string) =>
    getTicketsQuery(tripId ?? String(getTripId()));
  return {
    createTicket,
    getTickets,
    deleteTicket,
    updateMembers
  };
});
