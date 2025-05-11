import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Expense } from "@/types/interface";

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
