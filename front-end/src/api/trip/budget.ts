import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Budget } from "@/type/interface";

import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";

export const saveBudget = async (newBudget:Budget,param: Record<string, string>={}) => {
   if (APP_MODE_DEV) {
       const { setBudget } = useMockupStore();
       const setting = setBudget(newBudget, newBudget.trip);
       console.log(setting);
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
      return;
    }
  
    return data;
  };