import { useMutation } from "@tanstack/vue-query";
import { saveBudget } from "@/api";
import { useQueryClient } from "@tanstack/vue-query";
import router from "@/router";
import { useNotificationStore } from "@/stores";
import { getExpensesQuery, getMutationExpenseCreate } from "@/api/services/expenseQuery";
import {getMutationExpenseDelete} from "@/api/services/expenseQuery"
export const useBudget = (tripId:Function) => {
  const notification = useNotificationStore();
  const queryClient = useQueryClient();
  const createExpense = getMutationExpenseCreate({
          notification,
          queryClient,
          successMessage: "Pomyślnie usunięto wydatek",
          errorMessage: "Nie udało się usunąć wydatek",
  });
  const deleteExpense = getMutationExpenseDelete({
          notification,
          queryClient,
          successMessage: "Pomyślnie usunięto wydatek",
          errorMessage: "Nie udało się usunąć wydatek",
      })
  const getExpenseByTrip = (id?: number) => {
    const {
      data: expensesByTrip,
      isLoading: isLoading_expenses,
      error: error_expenses,
    } = getExpensesQuery(id ?? tripId());

    return {
      expensesByTrip,
      isLoading_expenses,
      error_expenses
    };
  };

  return {
    createExpense,
    getExpenseByTrip: getExpenseByTrip,
    deleteExpense
  };
};