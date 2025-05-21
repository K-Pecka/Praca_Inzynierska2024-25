import {useMutation, useQueryClient} from "@tanstack/vue-query";
import {useNotificationStore} from "@/stores";
import { useRoleStore } from "@/stores/auth/useRoleStore";
import { getTripQuery,getTripDetailsQuery, getMutationCreate, getMutationDelete,getMutationUpdate, getMutationUpdateBudget } from "@/api/services/tripQuery";
export const useTrips = (tripId:Function) => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();
    const roleStore = useRoleStore();
    const getTrips = (role?:string) => {
        const {data:trips,isLoading:isLoading_trips,error:error_trips} =  getTripQuery(role || roleStore.getRole())
        return {trips,isLoading_trips,error_trips}
     }

    const getTripDetails = (id?: number) => {
        const {data:trip,isLoading:isLoading_trip,error:error_trip} =  getTripDetailsQuery(id ?? tripId())
        return {trip,isLoading_trip,error_trip,}
    }

    const deleteTrip = getMutationDelete({
        notifications,
        queryClient,
        successMessage: "Pomyślnie usunięto wycieczkę",
        errorMessage: "Nie udało się usunąć wycieczki",
    })

    const createTrip = getMutationCreate({
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
