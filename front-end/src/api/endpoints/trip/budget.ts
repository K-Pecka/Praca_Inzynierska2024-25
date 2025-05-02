import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Budget, Expense } from "@/types/interface";

export const saveBudget = async (newBudget:Budget,param: Record<string, string>={}) => {
  const { data, error } = await fetchData(
      setParam(apiEndpoints.budget.update, {tripId: String(newBudget.trip)}),
      { body: JSON.stringify(newBudget) },
      "PATCH"
    );
    if (error) {
      throw new Error(error);
    }

    return data;
  };
export const createExpenseMutation = async (newExpense:Expense,param: Record<string, string>={}) => {
  const { data, error } = await fetchData(
      setParam(apiEndpoints.expense.create, {tripId: String(newExpense.trip)}),
      { body: JSON.stringify(newExpense) },
      "POST"
    );
    if (error) {
      throw new Error(error);
    }

    return {tripId: String(newExpense.trip)};
  }
