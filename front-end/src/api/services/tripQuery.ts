import { useMutation, useQuery } from "@tanstack/vue-query";
import type { Budget, Trip,TripData } from "@/types";
import {
  fetchTrips,
  fetchTrip,
  deleteTrip,
  createTrip,
  updateTrip,
  saveBudget,
} from "@api";
import { fetchUserRole } from "@/api/endpoints/auth";
import router from "@/router";
import { useQueryClient } from "@tanstack/vue-query";
import { useRoleStore } from "@/stores/auth/useRoleStore";
import { useAuthStore } from "@/stores";

export const getTripQuery = (role: string) => {
  return useQuery<TripData, Error, TripData>({
    queryKey: ["trips", role],
    queryFn: async () => {
      const queryClient = useQueryClient();
      const roleStore = useRoleStore();
      const authStore = useAuthStore();
      const cached = queryClient.getQueryData(["trips", role]);
      if (!cached) {
        let profile = await fetchUserRole(role);
        authStore.setActiveProfile(profile.id);
        roleStore.setRole(role);
      }
      return fetchTrips();
    },
    staleTime: 1000 * 60,
    gcTime: 1000 * 60 * 30,
  });
};
export const getTripDetailsQuery = (id: number) => {
  return useQuery<Trip, Error, Trip, [string, number]>({
    queryKey: ["trip", id],
    queryFn: fetchTrip,
    enabled: !!id,
    staleTime: 1000 * 60,
    gcTime: 1000 * 60 * 30,
  });
};
export const getMutationCreate = (option: Record<string, any>) =>
  useMutation({
    mutationFn: createTrip,
    onSuccess: () => {
      router.back();
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["trips", String(option.getRole())],
      });
    },
    onError: (err: any) => {
      option.notifications.setErrorCurrentMessage(
        err?.["non_field_errors"][0] || option.errorMessage
      );
    },
  });
export const getMutationDelete = (option: Record<string, any>) =>
  useMutation({
    mutationFn: deleteTrip,
    onSuccess: ({tripId}) => {
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.setQueryData(
        ['trips', String(option.getRole())],
        (oldTrips: TripData | undefined) => {
          if (!oldTrips) return;
          const filteredTrips = oldTrips.results.filter(trip => {
            return trip.id !== Number(tripId);
          });

          return {
            ...oldTrips,
            results: filteredTrips,
          };
        }
      );
    },
    onError: (err) => {
      option.notifications.setErrorCurrentMessage(
        err?.message || option.errorMessage
      );
    },
  });
export const getMutationUpdate = (option: Record<string, any>) =>
  useMutation({
    mutationFn: ({ tripId, newData }: { tripId:string; newData: any }) =>
      updateTrip({ tripId }, newData),
    onSuccess: ({ tripId }) => {
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["trip", Number(tripId)],
      });
      router.push({ name: "tripDashboard" });
    },
    onError: (err: any) => {
      option.notifications.setErrorCurrentMessage(
        err?.message || option.errorMessage
      );
    }, 
  });
export const getMutationUpdateBudget = (option: Record<string, any>) =>
  useMutation({
    mutationFn: ({
      newBudget,
      param,
    }: {
      newBudget: Budget;
      param: Record<string, string>;
    }) => saveBudget(newBudget, param),
    onSuccess: ({ tripId }) => {
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["trip", Number(tripId)],
      });
    },
    onError: (err: any) => {
      option.notifications.setErrorCurrentMessage(
        err?.message || option.errorMessage
      );
    },
  });
