import { useMutation, useQuery } from "@tanstack/vue-query"
import {fetchUserById,updateUser} from "@/api";
import router from "@/router";


export const getMutationUpdateUser = (option: Record<string,any>) => useMutation({
    mutationFn: (user: { first_name?: string; last_name?: string; password?: string,password_confirm?: string }) =>
        updateUser(user),
    onSuccess: () => {
        option.notification.setSuccessCurrentMessage(option.successMessage);
        option.saveToken(null);
        router.push({ name: "logIn" });
    },
    onError: (err: any) => {
        option.notification.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});