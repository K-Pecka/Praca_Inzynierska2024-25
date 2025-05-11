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


interface DeleteExpenseInput {
  expenseId: number;
  tripId: number;
}

//@ts-ignore
export const fetchExpenseDelete: MutationFunction<null, DeleteExpenseInput> = async ({
  expenseId,
  tripId,
}) => {
  const param = { tripId: String(tripId), expenseId: String(expenseId) };
  const url = setParam(`${apiEndpoints.expense.delete}`, param);
  const { data, error } = await fetchData<null>(url, 'DELETE');

  if (error) throw new Error(error);
  return data;
};
