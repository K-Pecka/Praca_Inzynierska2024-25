import { useQuery, useMutation } from "@tanstack/vue-query";
import { fetchPlans,fetchPlanDetails, createPlan, deleteItinerary } from "@/api";
import type { Plan } from "@/types";
import router from "@/router";
export const getPlansQuery = (tripId: string) => {
  return useQuery<Plan[]>({
    queryKey: ["plans", tripId],
    queryFn: async () => (await fetchPlans({ tripId })) ?? [],
  });
};

export const getPlanDetailsQuery = (tripId:number,planId: number) => {
    return useQuery({
      queryKey: ["plan", tripId, planId],
      queryFn: () => fetchPlanDetails({tripId:String(tripId),planId:String(planId)}),
      enabled: !!planId && !!tripId,
    });
  };

export const getMutationAddPlan = (option: {
  notifications: any;
  queryClient: any;
  successMessage: string;
  errorMessage: string;
  tripId:string;
}) =>
  useMutation({
    mutationFn: ({ data }: { data: Plan }) =>
      createPlan(data, { tripId: option.tripId }),
    onSuccess: () => {
        router.push({ name: "plans" });
        option.queryClient.invalidateQueries({ queryKey: ["plans", Number(option.tripId)] });
        option.notifications.setSuccessCurrentMessage(option.successMessage);
    },
    onError: (err: any) => {
      option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
  });
export const getMutationDeleteItinerary = (option: {
  notifications: any;
  queryClient: any;
  successMessage: string;
  errorMessage: string;
  tripId:string;
}) =>
  useMutation({
    mutationFn: ({ planId }: { planId: string }) =>
      deleteItinerary({ tripId: option.tripId, planId }),
    onSuccess: () => {
      option.queryClient.invalidateQueries({ queryKey: ["plans", Number(option.tripId)] });
      option.notifications.setSuccessCurrentMessage(option.successMessage);
    },
    onError: (err: any) => {
      option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
  });
