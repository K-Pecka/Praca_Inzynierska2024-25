import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Budget, Expense } from "@/types/interface";

export const saveBudget = async (newBudget: Budget, param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.budget.update, { tripId: String(newBudget.trip) });

  const { data, error } = await fetchData(url, "PATCH", newBudget);

  if (error) {
    throw new Error(error);
  }

  return data;
};

export const createExpenseMutation = async (newExpense: Expense, param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.expense.create, { tripId: String(newExpense.trip) });

  const { data, error } = await fetchData(url, "POST", newExpense);

  if (error) {
    throw new Error(error);
  }

  return { tripId: String(newExpense.trip) };
};
