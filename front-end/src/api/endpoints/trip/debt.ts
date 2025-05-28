import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Debt, DebtResponse } from "@/types/interface";

export const fetchDebt = async (param: Record<string, string> = {}) => {
    const url = setParam(apiEndpoints.debt.all, param);
  
    const { data, error } = await fetchData<DebtResponse>(url, "GET");
    if (error) {
        throw error;
    }
    return data?.results;
}
export const fetchDebtCreate = async (newDebt: Debt) => {
  const url = setParam(apiEndpoints.debt.create, {tripId:String(newDebt.trip)});
  
  const { data, error } = await fetchData(url, "POST", newDebt);
  if (error) {
    throw error;
  }

  return String(newDebt.trip);
};
export const fetchRemoveMember = async (param: Record<string, string> = {}) => {
   const url = setParam(apiEndpoints.debt.removeMember, param);
   
   const { data, error } = await fetchData(url, "POST",{profile_id: param.profileId});
    if (error) {
        throw error;
    }
    return param.tripId;

}
export const fetchDebtDelete = async (param: Record<string, string> = {}) => {
   const url = setParam(apiEndpoints.debt.delete, param);
   
   const { data, error } = await fetchData(url, "DELETE");
    if (error) {
        throw error;
    }
    return data;

}