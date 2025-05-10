import { defineStore } from "pinia";
import { getTicketsQuery,createTicketMutation } from "@/api/services/ticketQuery";
export const useTicketStore = defineStore("ticket", () => {

    const createTicket = createTicketMutation;
    const getTickets = (tripId:string) => getTicketsQuery(tripId);

    return {
        createTicket,
        getTickets
    };
});
