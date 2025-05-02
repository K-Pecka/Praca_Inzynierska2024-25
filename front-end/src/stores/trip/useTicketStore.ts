import { defineStore } from "pinia";
import { ref } from "vue";
import { useUtilsStore } from "@/stores/utils/useUtilsStore";
import { getTicketsQuery,createTicketMutation } from "@/api/services/ticketQuery";
import { TicketData } from "@/types";
interface Ticket {
    type: string;
    name: string;
    date: string;
    time: string;
    assignedTo?: string[];
    file: File;
}

export const useTicketStore = defineStore("ticket", () => {
    const tickets = ref<Ticket[]>([]);

    const createTicket = createTicketMutation;
    const getTickets = () => getTicketsQuery();

    return {
        tickets,
        createTicket,
        getTickets
    };
});
