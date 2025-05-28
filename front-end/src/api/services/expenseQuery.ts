import { Expense } from "@/types";
import { useMutation, useQuery } from "@tanstack/vue-query";
import {
  fetchExpenseDelete,
  fetchExpenses,
  fetchExpenseCreate,
} from "@/api";

export const getExpensesQuery = (params: Record<string, string>, filters: Record<string, string>) => {
  return useQuery({
    queryKey: ["expense", params.tripId, JSON.stringify(filters)],
    queryFn: () => fetchExpenses(params, filters),
    enabled: !!params.tripId,
    select: (data: Expense[] | undefined) =>
      Array.isArray(data)
        ? data.filter((item): item is Expense => item !== undefined)
        : [],
  });
};


export const getMutationExpenseCreate = (option: Record<string, any>) =>
  useMutation({
    mutationFn: fetchExpenseCreate,
    onSuccess: ({tripId}) => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["expense", Number(tripId)],
      });
    },
    onError: (err: any) => {
      option.notification.setErrorCurrentMessage(err?.message || err?.['non_field_errors'][0] || "Błąd");
    },
  });
export const getMutationExpenseDelete = (option: Record<string, any>) =>
  useMutation({
    mutationFn: fetchExpenseDelete,
    onSuccess: ({ tripId }) => {
      option.notification.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["expense", Number(tripId)],
      });
    },
    onError: (err) => {
      option.notification.setErrorCurrentMessage(
        err?.message || option.errorMessage
      );
    },
  });
