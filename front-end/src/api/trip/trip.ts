import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Trip,NewTrip } from "@/type/interface";
export const fetchTrips = async () => {
  const { data, error } = await fetchData<Trip[]>(
    apiEndpoints.trip.all,
    {},
    "GET"
  );
  if (error) {
    return [];
  }
  if(!data){
    return [];
  }
  return data;
};
export const fetchTrip = async (param: Record<string, string>={}) => {
    const { data, error } = await fetchData<Trip>(
      setParam(apiEndpoints.trip.detail,param),
      {},
      "GET"
    );
    if (error) {
      return;
    }
  
    return data;
  };
export const deleteTrip = async (param: Record<string, string>={}) => {
  const { data, error } = await fetchData(
    setParam(apiEndpoints.trip.delete, param),
    {},
    "DELETE"
  );
  if (error) {
    throw new Error(error);
    
    return;
  }

  return data;
};
export const createTrip = async (newTrip:NewTrip,param: Record<string, string>={}) => {
    const { data, error } = await fetchData<NewTrip>(
      setParam(apiEndpoints.trip.create, param),
      { body: JSON.stringify(newTrip) },
      "POST"
    );
    if (error) {
      return;
    }
  
    return data;
  };

export const updateTrip = async (
    param: Record<string, string>,
    tripData: Partial<Trip>
) => {
    const url = setParam(apiEndpoints.trip.update, param);
    const { data, error } = await fetchData<Trip>(
        url,
        {
            body: JSON.stringify(tripData),
        },
        "PATCH"
    );

    if (error) {
        throw new Error(error);
    }
    return data;
};