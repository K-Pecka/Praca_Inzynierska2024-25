import { useMutation } from "@tanstack/vue-query";
import { saveBudget } from "@/api";
import router from "@/router";
import { useNotificationStore } from "@/stores";

export const useBudget = () => {
    const notifications = useNotificationStore();

    const tripMutationBudget = useMutation({
        mutationFn: saveBudget,
        onSuccess: () => {
            notifications.setSuccessCurrentMessage("Zapisano");
            router.push({ name: "tripDashboard" });
        },
        onError: (err: any) => {
            notifications.setErrorCurrentMessage(err?.message || "Błąd");
        },
    });

    return { tripMutationBudget };
};
