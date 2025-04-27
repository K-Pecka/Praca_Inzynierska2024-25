import { useMutation, useQuery } from "@tanstack/vue-query"
import type { TicketData } from "@/types";
import { fetchTicket as originalFetchTicket,createTicket } from "@/api";

const fetchTicket = async (): Promise<TicketData[]> => {
    const result = await originalFetchTicket();
    return result ?? [];
};

export const getTicketsQuery = () => {
    return useQuery<TicketData[], Error>({
        queryKey: ["ticket"],
        queryFn: fetchTicket,
    })
}
export const createTicketMutation = (formData: FormData) => useMutation({
    mutationFn: async (formData: FormData) => {
      // Wysyłamy plik na serwer za pomocą fetch
      return await createTicket(formData);
    },
    onSuccess: (data) => {
      console.log('Bilet został pomyślnie utworzony:', data);
    },
    onError: (error) => {
      console.error('Błąd podczas tworzenia biletu:', error);
    },
  });