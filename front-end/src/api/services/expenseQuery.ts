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

interface DeleteExpenseInput {
  expenseId: number;
  tripId: number;
}

export const getMutationDelete = (option: Record<string, any>) =>
  useMutation<null, Error, DeleteExpenseInput>({
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