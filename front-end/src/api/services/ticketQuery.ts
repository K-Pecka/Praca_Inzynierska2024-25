import { useMutation, useQuery } from "@tanstack/vue-query";
import type { TicketData } from "@/types";
import { fetchTicket as originalFetchTicket, createTicket } from "@/api";

const fetchTicket = async (tripId: string): Promise<TicketData[]> => {
  const result = await originalFetchTicket({ tripId });
  return Array.isArray(result) ? result : [];
};

export const getTicketsQuery = (tripId: string) => {
  return useQuery<TicketData[], Error>({
    queryKey: ["ticket", Number(tripId)],
    queryFn: () => fetchTicket(tripId),
    enabled: !!tripId,
  });
};

export const createTicketMutation = (option: Record<string, any>) =>
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
    onSuccess: () => {
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["ticket", option.tripId()],
      });
    },
    onError: (err) => {
      option.notifications.setErrorCurrentMessage(
        err?.message || option.errorMessage
      );
    },
  });
