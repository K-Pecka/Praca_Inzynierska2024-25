import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Budget, Expense } from "@/types/interface";

import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";

export const saveBudget = async (newBudget:Budget,param: Record<string, string>={}) => {
   if (APP_MODE_DEV) {
       const { setBudget } = useMockupStore();
       const setting = setBudget(newBudget, newBudget.trip);
       if(setting == null){
         throw new Error("Wystąpił błąd związany z aktualizacją budżetu");
       }
     } 
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
  if (APP_MODE_DEV) {
    return {tripId: String(newExpense.trip)};
  } 
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