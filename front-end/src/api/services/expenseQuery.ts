import { Expense } from "@/types";
import { useQuery } from "@tanstack/vue-query";
import { fetchExpenses } from "@/api";

export const getExpensesQuery = (id: number) => {
    return useQuery({
        queryKey: ["expense", id],
        queryFn: () => fetchExpenses(["expense", id]),
        enabled: !!id,
        select: (data: Expense[] | undefined) =>
            Array.isArray(data) ? data.filter((item): item is Expense => item !== undefined) : [],
    });
};