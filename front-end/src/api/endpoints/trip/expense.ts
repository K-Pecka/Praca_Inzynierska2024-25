import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Expense } from "@/types/interface";
export const fetchExpenses = async (queryKey: [string, number]) => {
    const [type, id] = queryKey;
  const param = { tripId: String(id) };
  const { data, error } = await fetchData<Expense[]>(
    setParam(apiEndpoints.expense.all, param),
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
