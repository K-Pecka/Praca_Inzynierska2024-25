import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Trip,NewTrip } from "@/types/interface";
import { QueryFunctionContext } from "@tanstack/vue-query";
export const fetchTrips = async () => {
  const { data, error } = await fetchData<Trip[]>(
    apiEndpoints.trip.all,
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }
  if(!data){
    return [];
  }
  return data;
};
export const fetchTrip = async ({ queryKey }: QueryFunctionContext<[string,number]>) => {
  const [_,tripId] = queryKey;
  const { data, error } = await fetchData<Trip>(
    setParam(apiEndpoints.trip.detail,{tripId:String(tripId)}),
    {},
    "GET"
  );
  if (error || !data) {
    ////console.log('Error: ', error)
    throw new Error(error);
  }

  return data;
};
export const deleteTrip = async (param: Record<string, string>={}) => {
  //console.log(setParam(apiEndpoints.trip.delete, param));
  const { data, error } = await fetchData(
    setParam(apiEndpoints.trip.delete, param),
    {},
    "DELETE"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
export const createTrip = async (newTrip:NewTrip,param: Record<string, string>={}) => {
    const { data, error } = await fetchData<NewTrip>(
      setParam(apiEndpoints.trip.create, param),
      { body: JSON.stringify({...newTrip,budget_amount:0}) },
      "POST"
    );
    if (error) {
      throw new Error(error);
    }

    return data;
  };

export const updateTrip = async (
    tripData: Partial<Trip>
) => {
  const param={tripId:String(tripData.id)}
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
    return {data,tripId:param.tripId};
};
