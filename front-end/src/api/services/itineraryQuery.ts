import { useMutation, useQuery } from "@tanstack/vue-query";
import type { ItineraryResponse,NewItinerary } from "@/types";
import { fetchItinerary, createItinerary, deleteItinerary } from "@/api";

import router from "@/router";

export const getItineraryQuery = (id: string) => {
  return useQuery<ItineraryResponse, Error, ItineraryResponse>({
    queryKey: ["plans", Number(id)],
    queryFn: () => fetchItinerary({ tripId: id }),
    staleTime: 1000 * 60,
    gcTime: 1000 * 60 * 30,
  });
};
export const getMutationCreate =  (option: Record<string, any>) => useMutation({
        mutationFn: ({ data, tripId }: { data: NewItinerary; tripId: number }) =>
            createItinerary(data, { tripId: String(tripId) }),
        onSuccess: ({tripId}) => {
            router.back();
            option.notifications.setSuccessCurrentMessage("Dodano plan");
            option.queryClient.invalidateQueries({ queryKey: ["plans", Number(tripId)] });
        },
        onError: () => {
            option.notifications.setErrorCurrentMessage("Błąd");
        },
    });
export const getMutationDelete = (option: Record<string, any>) =>
  useMutation({
        mutationFn: ({ tripId, itineraryId }: { tripId: string; itineraryId: string }) =>
            deleteItinerary({ tripId, itineraryId }),
        onSuccess: ({tripId}) => {
            option.notifications.setSuccessCurrentMessage("Pomyślnie usunięto plan");
            option.queryClient.invalidateQueries({ queryKey: ["plans", Number(tripId)] });
        },
        onError: (err) => option.notifications.setErrorCurrentMessage(err.message),
    });