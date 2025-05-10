import { useQueryClient } from "@tanstack/vue-query";
import {
  getPlansQuery,
  getMutationAddPlan,
  getMutationDeleteItinerary,
  getPlanDetailsQuery
} from "@/api/services/planQuery";
import { useNotificationStore } from "@/stores";
import { computed } from "vue";
import router from "@/router";

export const usePlans = (tripIdFn: () => string | number | undefined,planIdFn: () => string | number | undefined) => {
  const queryClient = useQueryClient();
  const notifications = useNotificationStore();
  const resolvedTripId = () => String(tripIdFn?.() ?? "");
  const resolvedPlanId = () => String(planIdFn?.() ?? "");
  const getPlans = (id?: string) => {
    const {
      data: plans,
      isLoading: isLoading_plans,
      error: error_plans,
    } = getPlansQuery(id || resolvedTripId());
    return { plans, isLoading_plans, error_plans };
  };
  const getPlanDetails = (tripId?:number,planId?:number)=>{
    const {
      data: plan,
      isLoading: isLoading_plan,
      error: error_plan,
    } = getPlanDetailsQuery((tripId || Number(resolvedTripId())),(planId || Number(resolvedPlanId())));
    return { plan, isLoading_plan, error_plan };
  }
  const deleteItinerary = getMutationDeleteItinerary({
    notifications,
    queryClient,
    successMessage: "Pomyślnie usunięto plan",
    errorMessage: "Nie udało się usunąć planu",
    tripId: String(resolvedTripId()),
  });

  const addPlan = getMutationAddPlan({
    notifications,
    queryClient,
    successMessage: "Dodano plan",
    errorMessage: "Nie udało się dodać planu",
    tripId: String(resolvedTripId()),
  });
  const planBtn = computed(() => [
    {
      title: "Zarządzaj planem",
      class: "primary",
      icon: "mdi-pencil",
      showIfOwner: true,
      onclick: (itineraryId: string) =>
        router.push({
          name: "ActivityView",
          params: { planId: itineraryId },
        }),
    },
    {
      title: "usuń plan",
      class: "red",
      icon: "mdi-trash-can-outline",
      showIfOwner: true,
      onclick: ( itineraryId: string) =>
        deleteItinerary.mutate({ planId: itineraryId }),
    },
    {
      title: "Podgląd planu",
      class: "primary",
      icon: "mdi-eye-outline",
      showIfOwner: false,
      onclick: ( itineraryId: string) =>
        router.push({
          name: "ActivityView",
          params: {planId: itineraryId },
        }),
    },
  ]);

  return { getPlans, deleteItinerary, addPlan,getPlanDetails, planBtn };
};
