import { defineStore } from "pinia";
import {
  getTicketsQuery,
  createTicketMutation,
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

  const getTickets = (tripId?: string) =>
    getTicketsQuery(tripId ?? String(getTripId()));
  return {
    createTicket,
    getTickets,
  };
});
