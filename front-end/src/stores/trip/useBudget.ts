import { useQueryClient } from "@tanstack/vue-query";
import { useNotificationStore } from "@/stores";
import {
  getExpensesQuery,
  getMutationExpenseCreate,
} from "@/api/services/expenseQuery";
import { getMutationExpenseDelete } from "@/api/services/expenseQuery";
import { Ref, unref, ref } from "vue";
export const useBudget = (tripId: Function) => {
  const filters = ref({});
  const notification = useNotificationStore();
  const queryClient = useQueryClient();
  const setFilters = (newFilters: Record<string, string | null>) => {
    filters.value = Object.fromEntries(
      Object.entries(newFilters).filter(([_, value]) => value !== null)
    );
  }
  const getFilters = () => filters.value
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
  });
  const getExpenseByTrip = () => {
    const {
      data: expensesByTrip,
      isLoading: isLoading_expenses,
      error: error_expenses,
      refetch: refetch_expenses
    } = getExpensesQuery({ tripId: tripId() }, unref(filters?.value) || {});
    return {
      expensesByTrip,
      isLoading_expenses,
      error_expenses,
      refetch_expenses
    };
  };

  return {
    createExpense,
    getExpenseByTrip: getExpenseByTrip,
    deleteExpense,
    setFilters,
    getFilters
  };
};
