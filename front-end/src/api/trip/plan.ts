import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Trip, NewTrip } from "@/type/interface";
export const fetchPlans = async (param: Record<string, string> = {}) => {
  const { data, error } = await fetchData<Trip[]>(
    setParam(apiEndpoints.plan.all, param),
    {},
    "GET"
  );
  if (error) {
    return;
  }

  return data;
};
export const fetchPlan = async () => {
  const { data, error } = await fetchData<Trip[]>(
    apiEndpoints.plan.detail,
    {},
    "GET"
  );
  if (error) {
    return;
  }

  return data;
};
export const deletePlan = async (param: Record<string, string> = {}) => {
  const { data, error } = await fetchData(
    setParam(apiEndpoints.plan.delete, param),
    {},
    "DELETE"
  );
  if (error) {
    return;
  }

  return data;
};
export const createPlan = async (
  newTrip: Trip,
  param: Record<string, string> = {}
) => {
  const { data, error } = await fetchData<NewTrip>(
    setParam(apiEndpoints.plan.create, param),
    { body: JSON.stringify(newTrip) },
    "POST"
  );
  if (error) {
    return;
  }

  return data;
};
