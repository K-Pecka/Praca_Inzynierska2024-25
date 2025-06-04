import {fetchSubscriptionCancel} from "@/api"
import { useMutation } from "@tanstack/vue-query";

export const subscriptionCancelMutation = (option: Record<string, any>) =>
  useMutation({
    mutationFn: fetchSubscriptionCancel,
    onSuccess: () => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.updateUser({subscription_cancelled:true})
    },
    onError: (err: any) => {
        console.log(option)
      option.notification.setErrorCurrentMessage(
        err?.error || err?.["non_field_errors"][0] || option.errorMessage
      );
    },
  });