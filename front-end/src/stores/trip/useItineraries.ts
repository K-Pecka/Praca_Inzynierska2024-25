import { useQueryClient } from "@tanstack/vue-query";
import { useNotificationStore } from "@/stores";
import {
  getItineraryQuery,
  getMutationCreate,
  getMutationDelete,
} from "@/api/services/itineraryQuery";



export const useItineraries = (tripId: Function) => {
  const queryClient = useQueryClient();
  const notifications = useNotificationStore();

  const getItineraries = (id?: string) => {
    const {
      data: itineraries,
      isLoading: isLoading_itineraries,
      error: error_itineraries,
    } = getItineraryQuery(id || tripId());
    return { itineraries, isLoading_itineraries, error_itineraries};
  };

  const deleteItinerary = getMutationDelete({
        notifications,
        queryClient,
        successMessage: "Pomyślnie usunięto plan",
        errorMessage: "Nie udało się usunąć planu",});

  const createItinerary = getMutationCreate({
        notifications,
        queryClient,
        successMessage: "Pomyślnie dodano nowy plan",
        errorMessage: "Nie udało się dodano nowy plan",});
  
  const handleDeleteItinerary = async (tripId: string, itineraryId: string) => {
    try {
      await deleteItinerary.mutateAsync({ tripId, itineraryId });
    } catch (err) {}
  };

  return { createItinerary, getItineraries, handleDeleteItinerary,deleteItinerary };
};
