import { Expense } from "@/types";
import {useMutation, useQuery, useQueryClient} from "@tanstack/vue-query";
import {fetchExpenseDelete, fetchActivityDelete, fetchExpenses} from "@/api";

export const getExpensesQuery = (id: number) => {
    return useQuery({
        queryKey: ["expense", id],
        queryFn: () => fetchExpenses(["expense", id]),
        enabled: !!id,
        select: (data: Expense[] | undefined) =>
            Array.isArray(data) ? data.filter((item): item is Expense => item !== undefined) : [],
    });
};


export const getMutationExpenseDelete = (option: Record<string, any>) =>
  useMutation({
    mutationFn: fetchExpenseDelete,
    onSuccess: (_data, variables) => {
      option.notifications.setSuccessCurrentMessage(option.successMessage);
      option.queryClient.invalidateQueries({
        queryKey: ["expense", variables.tripId, variables.expenseId],
      });
    },
    onError: (err) => {
      option.notifications.setErrorCurrentMessage(err?.message || option.errorMessage);
    },
  });