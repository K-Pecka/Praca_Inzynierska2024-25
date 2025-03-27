import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Budget } from "@/type/interface";
export const saveBudget = async (newBudget:Budget,param: Record<string, string>={}) => {
    const { data, error } = await fetchData(
      setParam(apiEndpoints.budget.update, {tripId: String(newBudget.trip)}),
      { body: JSON.stringify(newBudget) },
      "PATCH"
    );
    if (error) {
      return;
    }
  
    return data;
  };