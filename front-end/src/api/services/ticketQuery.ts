import { useMutation, useQuery } from "@tanstack/vue-query"
import type { TicketData } from "@/types";
import { fetchTicket as originalFetchTicket,createTicket,fetchDeleteTicket } from "@/api";

const fetchTicket = async (tripId: string): Promise<TicketData[]> => {
    const result = await originalFetchTicket({ tripId: tripId });
    return result ?? [];
};

export const getTicketsQuery = (tripId: string) => {
    return useQuery<TicketData[], Error>({
        queryKey: ["tickets", Number(tripId)],
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
export const deleteTicektMutation = (option: Record<string,any>) => useMutation({
    mutationFn: fetchDeleteTicket,
    onSuccess: () => {
        option.notifications.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["tickets",Number(option.tripId)]});
    },
    onError: (err) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});