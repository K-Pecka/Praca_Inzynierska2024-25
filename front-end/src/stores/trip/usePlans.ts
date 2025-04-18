import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { fetchPlans, createPlan, deleteItinerary } from "@/api";
import router from "@/router";
import { computed } from "vue";
import { Plan } from "@/type";
import { useNotificationStore } from "@/stores";

export const usePlans = () => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();

    const deleteItineraryMutation = useMutation({
        mutationFn: ({ tripId, planId }: { tripId: string; planId: string }) =>
            deleteItinerary({ tripId, planId }),
        onSuccess: (data) => {
            notifications.setSuccessCurrentMessage("Pomyślnie usunięto plan");
            queryClient.invalidateQueries({ queryKey: ["plans", data?.tripId] });
        },
        onError: (err) => notifications.setErrorCurrentMessage(err.message),
    });

    const handleDeleteItinerary = async (tripId: string, planId: string) => {
        try {
            await deleteItineraryMutation.mutateAsync({ tripId, planId });
        } catch (err) {}
    };

    const planMutationAdd = useMutation({
        mutationFn: ({ data, tripId }: { data: Plan; tripId: number }) =>
            createPlan(data, { tripId: String(tripId) }),
        onSuccess: () => {
            router.back();
            notifications.setSuccessCurrentMessage("Dodano plan");
        },
        onError: () => {
            notifications.setErrorCurrentMessage("Błąd");
        },
    });

    const getPlans = (id: string) =>
        useQuery({
            queryKey: ["plans", id],
            queryFn: () => fetchPlans({ tripId: id }),
        });

    const yourPlans = computed(() => ({
        btn: [
            {
                title: "Zarządzaj planem",
                class: ["primary"],
                img: "/picture/plan-edit.svg",
                onclick: (trip: string, id: string) =>
                    router.push({ name: "ActivityView", params: { tripId: trip, planId: id } }),
            },
            {
                title: "usuń plan",
                class: ["accent"],
                img: "/picture/plan-delete.svg",
                onclick: (tripId: string, itineraryId: string) =>
                    handleDeleteItinerary(tripId, itineraryId),
            },
        ],
        plans: getPlans,
    }));

    return { planMutationAdd, getPlans, yourPlans };
};
