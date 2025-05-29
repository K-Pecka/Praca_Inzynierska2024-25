import { useMutation, useQuery } from "@tanstack/vue-query";
import { fetchDebt, fetchDebtCreate,fetchRemoveMember,fetchDebtDelete } from "@/api";
import { DebtDetails } from "@/types";

export const getDebtQuery = (tripId: number) => {
  return useQuery<DebtDetails[]>({
    queryKey: ["debt", Number(tripId)],
    queryFn: () => fetchDebt({ tripId: String(tripId) }) as Promise<DebtDetails[]>,
    enabled: !!tripId,
  });
};
export const getMutationDebtCreate = (option: Record<string, any>) =>
  useMutation({
    mutationFn: fetchDebtCreate,
    onSuccess: (tripId) => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["debt", Number(tripId)],
      });
    },
    onError: (err: any) => {
      option.notification.setErrorCurrentMessage(
        err?.message || err?.["non_field_errors"][0] || "Błąd"
      );
    },
  });

export const getMutationRemoveMemberQuery = (option: Record<string, any>) =>
    useMutation({
    mutationFn: fetchRemoveMember,
    onSuccess: (tripId) => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["debt", Number(tripId)],
      });
    },
    onError: (err: any) => {
      option.notification.setErrorCurrentMessage(
        err?.detail || err?.["non_field_errors"][0] || "Błąd"
      );
    },
  });
export const getMutationDeleteDebt = (option: Record<string, any>) =>
    useMutation({
    mutationFn: fetchDebtDelete,
    onSuccess: ({tripId}) => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["debt", Number(tripId)],
      });
    },
    onError: (err: any) => {
      option.notification.setErrorCurrentMessage(
        err?.detail || err?.["non_field_errors"][0] || "Błąd"
      );
    },
  });
