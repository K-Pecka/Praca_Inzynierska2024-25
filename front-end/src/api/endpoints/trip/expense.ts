import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Expense } from "@/types/interface";
import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";
export const fetchExpenses = async (queryKey: [string, number]) => {
    const [type, id] = queryKey;
    if (APP_MODE_DEV) {
    return [
        {
            title: "jedzenie",
            amount: 10,
            currency: "PLN",
            date: "12-02-2022",
            user: 1,
            category: 2,
        },
        {
            title: "jedzenie",
            amount: 10,
            currency: "PLN",
            date: "12-02-2022",
            user: 1,
            category: 2,
        },
    ];
  }
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