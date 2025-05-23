import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { fetchPlans, createPlan, deleteItinerary } from "@/api";
import router from "@/router";
import { computed } from "vue";
import { Plan } from "@/types";
import { useNotificationStore } from "@/stores";

export const usePlans = (tripId:Function) => {
    const queryClient = useQueryClient();
    const notifications = useNotificationStore();

    const deleteItineraryMutation = useMutation({
        mutationFn: ({ tripId, planId }: { tripId: string; planId: string }) =>
            deleteItinerary({ tripId, planId }),
        onSuccess: ({tripId}) => {
            notifications.setSuccessCurrentMessage("Pomyślnie usunięto plan");
            queryClient.invalidateQueries({ queryKey: ["plans", Number(tripId)] });
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
        onSuccess: ({tripId}) => {
            router.back();
            notifications.setSuccessCurrentMessage("Dodano plan");
            queryClient.invalidateQueries({ queryKey: ["plans", Number(tripId)] });
        },
        onError: () => {
            notifications.setErrorCurrentMessage("Błąd");
        },
    });

    const getPlans = (id?: string) =>
        useQuery({
            queryKey: ["plans", Number(id ?? tripId())],
            queryFn: () => fetchPlans({ tripId: id ?? tripId() }),
        });

    const yourPlans = computed(() => ({
        btn: [
            {
              title: "Zarządzaj planem",
              class: "primary",
              icon: "mdi-pencil",
              showIfOwner: true,
              onclick: (tripId: string, itineraryId: string) =>
                  router.push({name: "ActivityView", params: {tripId: tripId, planId: itineraryId}}),
            },
            {
              title: "usuń plan",
              class: "red",
              icon: "mdi-trash-can-outline",
              showIfOwner: true,
              onclick: (tripId: string, itineraryId: string) =>
                  handleDeleteItinerary(tripId, itineraryId),
            },
            {
            title: "Podgląd planu",
            class: "primary",
            icon: "mdi-eye-outline",
            showIfOwner: false,
            onclick: (tripId: string, itineraryId: string) =>
              router.push({ name: "ActivityView", params: { tripId, planId: itineraryId } }),
            }
          ],
        plans: getPlans,
    }));

    return { planMutationAdd, getPlans, yourPlans, handleDeleteItinerary };
};

