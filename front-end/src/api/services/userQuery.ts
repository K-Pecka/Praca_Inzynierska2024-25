import { useMutation } from "@tanstack/vue-query"
import {updateUser,fetchDeleteUser} from "@/api";
import router from "@/router";


export const getMutationUpdateUser = (option: Record<string,any>) => useMutation({
    mutationFn: (user: { first_name?: string; last_name?: string; current_password?: string; password?: string,password_confirm: string }) =>
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
export const deleteUserMutation = (option: Record<string,any>) => useMutation({
    mutationFn: fetchDeleteUser,
    onSuccess: () => {
        option.notification.setSuccessCurrentMessage(option.successMessage);
        option.saveToken(null);
        option.saveUser(null);
        router.push({ name: "landing" });
    },
    onError: (err: any) => {
        option.notification.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
});