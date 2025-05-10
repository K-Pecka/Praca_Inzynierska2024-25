import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Plan, NewPlan } from "@/types/interface";
export const fetchPlans = async (param: Record<string, string> = {}) => {
  const { data, error } = await fetchData<Plan[]>(
    setParam(apiEndpoints.plan.all, param),
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
export const fetchPlanDetails = async (param:{tripId:string,planId:string}) => {
  const { data, error } = await fetchData<Plan>(
    setParam(apiEndpoints.plan.detail,param),
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
export const deleteItinerary = async (param: Record<string, string> = {}) => {
  const { data, error } = await fetchData(
    setParam(apiEndpoints.plan.delete, param),
    {},
    "DELETE"
  );
  console.log(param)
  if (error) {
    
    throw new Error(error);
  }

  return param;
};
export const createPlan = async (
  newPlan: Plan,
  param: Record<string, string> = {}
) => {
  const { data, error } = await fetchData<NewPlan>(
    setParam(apiEndpoints.plan.create, param),
    { body: JSON.stringify(newPlan) },
    "POST"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
