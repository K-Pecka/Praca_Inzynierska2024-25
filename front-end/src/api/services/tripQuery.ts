import { useMutation, useQuery } from "@tanstack/vue-query"
import type { Trip } from "@/types";
import {fetchTrips, fetchTrip, deleteTrip, createTrip, updateTrip} from "@/api";
import router from "@/router";

export const getTripQuery = () => {
    return useQuery<Trip[], Error>({
        queryKey: ["trips"],
        queryFn: fetchTrips,
    })
}
export const getTripDetailsQuery = (id: number) => {
    return useQuery<Trip, Error, Trip, [string, number]>({
        queryKey: ["trip", id],
        queryFn: fetchTrip,
        enabled: !!id,
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