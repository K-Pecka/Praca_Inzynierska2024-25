import { Expense } from "@/types";
import { useMutation, useQuery } from "@tanstack/vue-query";
import {
  fetchExpenseDelete,
  fetchExpenses,
  fetchExpenseCreate,
} from "@/api";

export const getExpensesQuery = (id: number) => {
  return useQuery({
    queryKey: ["expense", id],
    queryFn: () => fetchExpenses(["expense", id]),
    enabled: !!id,
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
      option.notification.setErrorCurrentMessage(err?.message || "Błąd");
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
