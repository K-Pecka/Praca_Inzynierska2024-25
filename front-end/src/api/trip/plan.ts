import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Trip, NewTrip } from "@/type/interface";
import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";
export const fetchPlans = async (param: Record<string, string> = {}) => {
  if (APP_MODE_DEV) {
    const { getPlans } = useMockupStore();
    const plan = getPlans(Number(param.tripId));
    if(plan == null){
      throw new Error("Brak stworzonych dla tej wycieczki");
    }
    return plan;
  }
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
export const deleteItinerary = async (param: Record<string, string> = {}) => {
  if (APP_MODE_DEV) {
    const { deletePlanMockUp } = useMockupStore();
    const plan = deletePlanMockUp(Number(param.itineraryId));
    if(plan == null){
      throw new Error("Wystąpił błąd związany z usunięciem planu");
    }
    return param;
  }
  const { data, error } = await fetchData(
    setParam(apiEndpoints.plan.delete, param),
    {},
    "DELETE"
  );
  if (error) {
    return;
  }

  return param;
};
export const createPlan = async (
  newTrip: Trip,
  param: Record<string, string> = {}
) => {
  if (APP_MODE_DEV) {
    const { createPlanMockUp } = useMockupStore();
    const plan = createPlanMockUp(newTrip,param);
    if(plan == null){
      throw new Error("Wystąpił błąd związany z dadaniem planu");
    }
    return param;
  }
  const { data, error } = await fetchData<NewTrip>(
    setParam(apiEndpoints.plan.create, param),
    { body: JSON.stringify(newTrip) },
    "POST"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
