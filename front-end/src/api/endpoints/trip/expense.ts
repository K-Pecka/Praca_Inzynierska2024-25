import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Expense } from "@/types/interface";
import {MutationFunction} from "@tanstack/vue-query";

export const fetchExpenses = async (queryKey: [string, number]) => {
  const [, id] = queryKey;
  const param = { tripId: String(id) };
  const url = setParam(apiEndpoints.expense.all, param);

  const { data, error } = await fetchData<Expense[]>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data;
};
export const fetchExpenseCreate = async (newExpense: Expense, param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.expense.create, {tripId:String(newExpense.trip)});
  
  const { data, error } = await fetchData(url, "POST", newExpense);
  if (error) {
    throw new Error(error);
  }

  return {tripId:String(newExpense.trip)};
};
export const fetchExpenseDelete = async (param: Record<string, string> = {}) => {

  const url = setParam(`${apiEndpoints.expense.delete}`, param);
  const { data, error } = await fetchData<null>(url, 'DELETE');

  if (error) throw new Error(error);
  return param;
};
