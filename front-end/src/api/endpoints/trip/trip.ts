import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Trip,TripData, NewTrip } from "@/types/interface";
import { QueryFunctionContext } from "@tanstack/vue-query";
import { Budget } from "@/types/interface";


export const fetchTrips = async () => {
    const { data, error } = await fetchData<TripData>(apiEndpoints.trip.all, "GET");

    if (error) {
        throw new Error(error);
    }

    return data?.results || [];
};

export const fetchTrip = async ({ queryKey }: QueryFunctionContext<[string, number]>) => {
    const [, tripId] = queryKey;
    const url = setParam(apiEndpoints.trip.detail, { tripId: String(tripId) });

    const { data, error } = await fetchData<Trip>(url, "GET");

    if (error || !data) {
        throw new Error(error);
    }

    return data;
};

export const deleteTrip = async (param: Record<string, string> = {}) => {
    const url = setParam(apiEndpoints.trip.delete, param);

    const { data, error } = await fetchData(url, "DELETE");

    if (error) {
        throw error;
    }

    return param;
};

export const createTrip = async (newTrip: NewTrip, param: Record<string, string> = {}) => {
    const url = setParam(apiEndpoints.trip.create, param);

    const { data, error } = await fetchData<Trip>(
        url,
        "POST",
        { ...newTrip, budget_amount: 0 }
    );
    if (error) {
        throw error;
    }

    return data;
};

export const updateTrip = async (
    param: Record<string, string>,
    tripData: Partial<Trip>
) => {
    const url = setParam(apiEndpoints.trip.update, param);

    const { error } = await fetchData<Trip>(url, "PATCH", tripData);

    if (error) {
        throw new Error(error);
    }

    return param;
};
export const saveBudget = async (newBudget: Budget, param: Record<string, string> = {}) => {
  const url = setParam(apiEndpoints.trip.update, param);

  const { error } = await fetchData(url, "PATCH", newBudget);

  if (error) {
    throw new Error(error);
  }

  return param;
};