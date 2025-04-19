import {useQuery, useMutation, useQueryClient} from "@tanstack/vue-query";
import {fetchTrips, fetchTrip, deleteTrip, createTrip, updateTrip} from "@/api";
import router from "@/router";
import {computed} from "vue";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {useNotificationStore} from "@/stores";
import {Role} from "@/type/enum";
import type { Trip } from "@/type";

export const useTrips = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();
    const {getRole} = useRoleStore();

    const getTrips = () =>
        useQuery({
            queryKey: ["trips"],
            queryFn: fetchTrips,
        });

    const getTripDetails = (id: number) => {
        return useQuery<Trip, Error, Trip, [string, number]>({
            queryKey: ["trip", id],
            queryFn: fetchTrip,
            //keepPreviousData: true,
        });
    };

    const deleteTripMutation = useMutation({
        mutationFn: deleteTrip,
        onSuccess: () => {
            notifications.setSuccessCurrentMessage("Pomyślnie usunięto wycieczkę");
            queryClient.invalidateQueries({queryKey: ["trips"]});
        },
        onError: (err) => {
            notifications.setErrorCurrentMessage(err.message);
        },
    });

    const tripMutationAdd = useMutation({
        mutationFn: createTrip,
        onSuccess: () => {
            router.back();
            notifications.setSuccessCurrentMessage("Dodano wycieczkę");
        },
        onError: (err: any) => {
            notifications.setErrorCurrentMessage(err?.message || "Błąd");
        },
    });

    const tripMutationUpdate = useMutation({
        mutationFn: ({tripId, newData}: { tripId: string; newData: any }) =>
            updateTrip({tripId}, newData),
        onSuccess: () => {
            notifications.setSuccessCurrentMessage("Zaktualizowano wycieczkę");
        },
        onError: (err: any) => {
            notifications.setErrorCurrentMessage(err?.message || "Błąd");
        },
    });

    const handleDeleteTrip = async (id: string) => {
        try {
            await deleteTripMutation.mutateAsync({tripId: id});
        } catch {
        }
    };

    const yourTrips = computed(() => {
        const btnPath = getRole() === Role.TURIST ? "tripDashboard" : "tripDashboardGuide";

        return {
            btn: [
                {
                    title: "Zarządzaj wycieczką",
                    class: ["primary"],
                    onclick: (id: string) =>
                        router.push({name: btnPath, params: {tripId: id}}),
                },
                {
                    title: "Usuń wycieczkę",
                    class: ["accent"],
                    onclick: (id: string) => handleDeleteTrip(id),
                },
            ],
            trips: getTrips,
        };
    });

    return {getTrips, getTripDetails, yourTrips, tripMutationUpdate, tripMutationAdd};
};
