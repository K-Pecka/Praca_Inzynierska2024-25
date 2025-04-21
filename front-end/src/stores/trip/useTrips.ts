import {useQueryClient} from "@tanstack/vue-query";
import {computed} from "vue";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {useNotificationStore} from "@/stores";
import {Role} from "@/type/enum";
import type { Btn } from "@/type";
import { getTripQuery,getTripDetailsQuery, getMutationCreate, getMutationDelete,getMutationUpdate } from "@/api/serwis/tripQuery";
import { getBtn } from "@/dataStorage/page/panel";
import { TypeOfButton } from "@/type/enum";
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
          btnPath: getRole() === Role.TURIST ? "tripDashboard" : "tripDashboardGuide",
          handleDeleteTrip: (id: string) => deleteTripMutation.mutateAsync({ tripId: id }).catch(() => {}),
        }),
        trips: getTrips,
      }));

    return {getTrips, getTripDetails, yourTrips, tripMutationUpdate, tripMutationAdd};
};
