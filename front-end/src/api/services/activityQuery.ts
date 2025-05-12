import { useMutation } from "@tanstack/vue-query"
import {fetchActivityDelete} from "@/api";

export const getMutationDelete = (option: Record<string,any>) => useMutation({
    mutationFn: fetchActivityDelete,
    onSuccess: (data) => {
        option.notification.setSuccessCurrentMessage(option.successMessage);
        option.queryClient.invalidateQueries({queryKey: ["activities", Number(data.tripId), Number(data.planId)]});
    },
    onError: (err) => {
        option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});