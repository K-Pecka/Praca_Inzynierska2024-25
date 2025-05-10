import { getTicketsQuery,createTicketMutation,deleteTicektMutation } from "@/api/services/ticketQuery";

export const useTicket = (tripId:Function) => {
    const createTicket = createTicketMutation;
    const getTickets = (id?:string) => {
        const {data:tickets,isLoading:isLoading_ticekts,isError:isError_tickets} = getTicketsQuery(id ?? tripId());
        console.log(tickets)
        return {tickets,isLoading_ticekts,isError_tickets};
    }
    const deleteTicket = deleteTicektMutation;
    return {
        deleteTicket,
        createTicket,
        getTickets
    };
};
