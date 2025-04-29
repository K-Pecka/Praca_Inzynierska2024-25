import {useQueryClient} from "@tanstack/vue-query";
import {computed} from "vue";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {useNotificationStore} from "@/stores";
import {Role} from "@/types/enum";
import type { Btn } from "@/types";
import { getTripQuery,getTripDetailsQuery, getMutationCreate, getMutationDelete,getMutationUpdate } from "@/api/services/tripQuery";
import { getBtn } from "@/data/page/panel";
import { TypeOfButton } from "@/types/enum";
export const useTrips = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();
    const {getRole} = useRoleStore();

    const getTrips = () => getTripQuery();

    const getTripDetails = (id: number) => getTripDetailsQuery(id)

    const deleteTripMutation = getMutationDelete({
        notifications,
        successMessage: "Pomyślnie usunięto wycieczkę",
        errorMessage: "Nie udało się usunąć wycieczki",
    })

    const tripMutationAdd = getMutationCreate({
        notifications,
        queryClient,
        successMessage: "Dodano wycieczkę",
        errorMessage: "Nie udało się dodać wycieczki",
    })

    const tripMutationUpdate = getMutationUpdate({
        notifications,
        queryClient,
        successMessage: "Zaktualizowano wycieczkę",
        errorMessage: "Nie udało się zaktualizować wycieczki",
    })

    const yourTrips = computed(() => ({
        btn: getBtn({
          filter: (el: Btn) => el.type == TypeOfButton.TRIP,
          btnPath: getRole() === Role.TURIST ? "Dashboard" : "tripDashboardGuide",
          handleDeleteTrip: (id: string) => deleteTripMutation.mutateAsync({ tripId: id }).catch(() => {}),
        }),
        trips: getTrips,
      }));

    return {getTrips, getTripDetails, yourTrips, tripMutationUpdate, tripMutationAdd};
};
