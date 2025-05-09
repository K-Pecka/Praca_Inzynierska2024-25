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
export const fetchPlan = async () => {
  const { data, error } = await fetchData<Plan>(
    apiEndpoints.plan.detail,
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
