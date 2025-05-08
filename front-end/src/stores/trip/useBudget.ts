import { useMutation } from "@tanstack/vue-query";
import { saveBudget, createExpenseMutation } from "@/api";
import { useQueryClient } from "@tanstack/vue-query";
import router from "@/router";
import { useNotificationStore } from "@/stores";
import { getExpensesQuery } from "@/api/services/expenseQuery";
export const useBudget = (tripId:Function) => {
  const notifications = useNotificationStore();
  const queryClient = useQueryClient();
  const tripMutationBudget = useMutation({
    mutationFn: saveBudget,
    onSuccess: () => {
      notifications.setSuccessCurrentMessage("Zapisano");
      router.push({ name: "Dashboard" });
    },
    onError: (err: any) => {
      notifications.setErrorCurrentMessage(err?.message || "Błąd");
    },
  });
  const createExpense = useMutation({
    mutationFn: createExpenseMutation,
    onSuccess: (data) => {
      notifications.setSuccessCurrentMessage("Wydatek został zapisany");
      queryClient.invalidateQueries({ queryKey: ["expense", data?.tripId] });
    },
    onError: (err: any) => {
      notifications.setErrorCurrentMessage(err?.message || "Błąd");
    },
  });
  const getExpensByTrip = (id?:number) => {
    const { data: expensesByTrip, isLoading: isLoading_expenses,error:error_expenses } =
      getExpensesQuery(id ?? tripId());
    return {
      expensesByTrip,
      isLoading_expenses,
      error_expenses,
    };
  };

  return {
    tripMutationBudget,
    createExpense,
    getExpensByTrip,
  };
};