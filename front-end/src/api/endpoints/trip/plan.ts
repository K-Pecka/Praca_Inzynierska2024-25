import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Plan, NewPlan,PlanResponse } from "@/types/interface";

export const fetchPlans = async (param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.plan.all, param);

  const { data, error } = await fetchData<PlanResponse>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data?.results;
};

export const fetchPlan = async () => {
  const { data, error } = await fetchData<Plan>(apiEndpoints.plan.detail, "GET");

  if (error) {
    throw new Error(error);
  }

  return data;
};

export const deleteItinerary = async (param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.plan.delete, param);

  const { data, error } = await fetchData(url, "DELETE");

  if (error) {
    throw new Error(error);
  }

  return param;
};

export const createPlan = async (
    newPlan: Plan,
    param: Record<string, string> = {}
) => {
  const url = setParam(apiEndpoints.plan.create, param);

  const { data, error } = await fetchData<NewPlan>(url, "POST", newPlan);

  if (error) {
    throw new Error(error);
  }

  return param;
};
