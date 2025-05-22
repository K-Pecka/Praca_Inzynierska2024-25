import { useMutation, useQuery} from "@tanstack/vue-query"
import type { Budget, Trip } from "@/types";
import {fetchTrips, fetchTrip, deleteTrip, createTrip, updateTrip, saveBudget} from "@api";
import { fetchUserRole } from "@/api/endpoints/auth";
import router from "@/router";
import { useQueryClient } from "@tanstack/vue-query";
import { useRoleStore } from "@/stores/auth/useRoleStore";

export const getTripQuery = (role: string) => {
  return useQuery<Trip[], Error, Trip[]>({
    queryKey: ['trips', role],
    queryFn: async () => {
        const queryClient = useQueryClient();
        console.log("Fetching trips for role:", ['trips', role]);
      const roleStore = useRoleStore();
      const cached = queryClient.getQueryData(['trips', role]);

      if (!cached) {
        await fetchUserRole(role);
        roleStore.setRole(role);
      }

      return fetchTrips();
    },
    staleTime: 1000 * 60,
    gcTime: 1000 * 60 * 30
  });
};
export const getTripDetailsQuery = (id: number) => {
    return useQuery<Trip, Error, Trip, [string, number]>({
        queryKey: ["trip", id],
        queryFn: fetchTrip,
        enabled: !!id,
        staleTime: 1000 * 60,
        gcTime: 1000 * 60 * 30
    })
}
export const getMutationCreate = (option: Record<string,any>) => useMutation({
    mutationFn: createTrip,
    onSuccess: () => {
        router.back();
        option.notifications.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["trips"]});
    },
    onError: (err: any) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});
export const getMutationDelete = (option: Record<string,any>) => useMutation({
    mutationFn: deleteTrip,
    onSuccess: () => {
        option.notifications.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["trips"]});
    },
    onError: (err) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});
export const getMutationUpdate = (option: Record<string,any>)=>useMutation({
    mutationFn: ({tripId, newData}: { tripId: string; newData: any }) =>
        updateTrip({tripId}, newData),
    onSuccess: () => {
        option.notifications.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["trips"]});
    },
    onError: (err: any) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});