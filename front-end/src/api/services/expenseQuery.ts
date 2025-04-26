import { Expense } from "@/types"
import { useMutation, useQuery } from "@tanstack/vue-query"
import { fetchExpenses } from "@/api"
export const getExpensesQuery = (id: number) => {
    return useQuery<Expense[], Error, Expense[] | [], [string, number]>({
        queryKey: ["expense", id],
        queryFn: async (context) => {
            const result = await fetchExpenses(context.queryKey);
            return Array.isArray(result) ? result.filter((item): item is Expense => item !== undefined) : [];
        },
    })
}