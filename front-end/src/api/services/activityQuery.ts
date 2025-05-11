import {fetchActivityDelete} from "@/api/endpoints/trip/activity"
import { useMutation, useQuery } from "@tanstack/vue-query"
import router from "@/router";

export const getMutationDelete = (option: Record<string,any>) => useMutation({
    mutationFn: fetchActivityDelete,
    onSuccess: (data) => {
        option.notifications.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["activities", Number(data.tripId), Number(data.itineraryId)]});
    },
    onError: (err) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});