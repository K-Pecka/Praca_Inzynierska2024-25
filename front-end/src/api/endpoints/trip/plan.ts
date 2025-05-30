import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Itinerary, NewItinerary,ItineraryResponse } from "@/types/interface";

export const fetchItinerary = async (param: Record<string, string> = {}):Promise<ItineraryResponse> => {
  const url = setParam(apiEndpoints.plan.all, param);

  const { data, error } = await fetchData<ItineraryResponse>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data || {results:[]};
};

export const deleteItinerary = async (param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.plan.delete, param);

  const { data, error } = await fetchData(url, "DELETE");

  if (error) {
    throw new Error(error);
  }

  return param;
};

export const createItinerary = async (
    newPlan: NewItinerary,
    param: Record<string, string> = {}
) => {
  const url = setParam(apiEndpoints.plan.create, param);

  const { data, error } = await fetchData<NewItinerary>(url, "POST", newPlan);

  if (error) {
    throw new Error(error);
  }

  return param;
};
