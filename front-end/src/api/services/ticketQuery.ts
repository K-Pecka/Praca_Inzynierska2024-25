import { useMutation, useQuery } from "@tanstack/vue-query"
import type { TicketData } from "@/types";
import { fetchTicket as originalFetchTicket,createTicket } from "@/api";

const fetchTicket = async (tripId: string): Promise<TicketData[]> => {
    const result = await originalFetchTicket({ tripId: tripId });
    return result ?? [];
};

export const getTicketsQuery = (tripId: string) => {
    return useQuery<TicketData[], Error>({
        queryKey: ["ticket", tripId],
        queryFn: ({ queryKey }) => {
            const [, tripId] = queryKey as [string, string];
            return fetchTicket(tripId);
        },
    });
};
export const createTicketMutation = (formData: FormData,params:Record<string, string>) => useMutation({
    mutationFn: async (formData: FormData) => {
      return await createTicket(formData, params);
    },
    onSuccess: (data) => {
      ////console.log('Bilet został pomyślnie utworzony:', data);
    },
    onError: (error) => {
      //console.error('Błąd podczas tworzenia biletu:', error);
    },
  });