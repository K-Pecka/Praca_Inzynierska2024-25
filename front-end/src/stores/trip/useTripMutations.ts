import {useMutation} from "@tanstack/vue-query";
import {saveBudget, updateTrip, createTrip} from "@/api";
import router from "@/router";
import {useNotificationStore} from "@/stores";

export const useTripMutations = () => {
    const notifications = useNotificationStore();

    const tripMutationBudget = useMutation({
        mutationFn: saveBudget,
        onSuccess: () => {
            notifications.setSuccessCurrentMessage("Zapisano");
            router.push({name: "tripDashboard"});
        },
        onError: (err: any) => {
            notifications.setErrorCurrentMessage(err?.message || "Błąd");
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

    return {tripMutationAdd, tripMutationUpdate, tripMutationBudget};
};
