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
