import { defineStore } from "pinia";
import { getTicketsQuery,createTicketMutation } from "@/api/services/ticketQuery";
import { useUtilsStore } from "../utils/useUtilsStore";
export const useTicketStore = defineStore("ticket", () => {
    const {getTripId} = useUtilsStore()
    const createTicket = createTicketMutation;
    const getTickets = (tripId?:string) => getTicketsQuery(tripId ?? String(getTripId()));

    return {
        createTicket,
        getTickets
    };
});
