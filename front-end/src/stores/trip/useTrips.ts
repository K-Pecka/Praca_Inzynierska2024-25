import {useQueryClient} from "@tanstack/vue-query";
import {useNotificationStore, useUtilsStore} from "@/stores";
import { getTripQuery,getTripDetailsQuery, getMutationCreate, getMutationDelete,getMutationUpdate, getMutationUpdateBudget } from "@/api/services/tripQuery";

export const useTrips = (tripId:Function) => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();
    const {getRole} = useUtilsStore();

    const getTrips = (role?:string) => {
        const {data:trips,isLoading:isLoading_trips,error:error_trips,refetch:refetch_trips} =  getTripQuery(role || getRole())
        return {trips,isLoading_trips,error_trips,refetch_trips}
     }

    const getTripDetails = (id?: number) => {
        const {data:trip,isLoading:isLoading_trip,error:error_trip} =  getTripDetailsQuery(id ?? tripId())
      
        return {trip,isLoading_trip,error_trip}
    }

    const deleteTrip = getMutationDelete({
        getRole: () => getRole(),
        notifications,
        queryClient,
        successMessage: "Pomyślnie usunięto wycieczkę",
        errorMessage: "Nie udało się usunąć wycieczki",
    })

    const createTrip = getMutationCreate({
        getRole: () => getRole(),
        notifications,
        queryClient,
        successMessage: "Dodano wycieczkę",
        errorMessage: "Nie udało się dodać wycieczki",
    })

    const updateTrip = getMutationUpdate({
        notifications,
        queryClient,
        successMessage: "Zaktualizowano wycieczkę",
        errorMessage: "Nie udało się zaktualizować wycieczki",
    })
    const updateTripBudget = getMutationUpdateBudget({
        notifications,
        queryClient,
        successMessage: "Budżet został zaktualizowany",
        errorMessage: "Nie udało się zaktualizować budżetu",
      });
    return {getTrips, getTripDetails, deleteTrip, updateTrip, createTrip,updateTripBudget};
};
