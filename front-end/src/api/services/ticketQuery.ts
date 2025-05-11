import { useMutation, useQuery } from "@tanstack/vue-query";
import type { TicketData } from "@/types";
import { fetchTicket as originalFetchTicket, createTicket } from "@/api";

const fetchTicket = async (tripId: string): Promise<TicketData[]> => {
    const result = await originalFetchTicket({ tripId });
    return Array.isArray(result) ? result : [];
};

export const getTicketsQuery = (tripId: string) => {
    return useQuery<TicketData[], Error>({
        queryKey: ["ticket", tripId],
        queryFn: () => fetchTicket(tripId),
        enabled: !!tripId,
    });
};

export const createTicketMutation = () =>
    useMutation({
        mutationFn: async ({
                               formData,
                               params,
                           }: {
            formData: FormData;
            params: Record<string, string>;
        }) => {
            return await createTicket(formData, params);
        },
    });