import { useTripStore } from "@/stores";
import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Expense,ExpenseResponse } from "@/types/interface";

export const fetchExpenses = async (param: Record<string, string>, filters?: Record<string, string>) => {
  const {budget} = useTripStore()
  const params = new URLSearchParams();

  Object.entries(budget.getFilters() ?? {}).forEach(([key, value]) => {
    if (value) params.append(key, String(value));
  });

  const url = `${setParam(apiEndpoints.expense.all,param)}?${params.toString()}`;

  const { data, error } = await fetchData<ExpenseResponse>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data?.results;
};

export const fetchExpenseCreate = async (newExpense: Expense, param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.expense.create, {tripId:String(newExpense.trip)});
  
  const { data, error } = await fetchData(url, "POST", newExpense);
  if (error) {
    throw error;
  }

  return {tripId:String(newExpense.trip)};
};
export const fetchExpenseDelete = async (param: Record<string, string> = {}) => {

  const url = setParam(`${apiEndpoints.expense.delete}`, param);
  const { data, error } = await fetchData<null>(url, 'DELETE');

  if (error) throw new Error(error);
  return param;
};
