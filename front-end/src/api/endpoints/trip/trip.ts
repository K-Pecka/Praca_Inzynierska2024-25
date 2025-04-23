import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Trip,NewTrip } from "@/type/interface";
import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";
import { QueryFunctionContext } from "@tanstack/vue-query";
export const fetchTrips = async () => {
  if (APP_MODE_DEV) {
    const { getTrips } = useMockupStore();
    const trips = getTrips();
    if(trips == null){
      throw new Error("Brak wycieczek");
    }
    return trips;
  }
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
  if (APP_MODE_DEV) {
    const { getTrip } = useMockupStore();
    const trip = getTrip(Number(tripId));
    if(trip == null){
      throw new Error("Podana wycieczka nie istnieje");
    }
    return trip;
  }
    const { data, error } = await fetchData<Trip>(
      setParam(apiEndpoints.trip.detail,{tripId:String(tripId)}),
      {},
      "GET"
    );
    if (error || !data) {
      throw new Error(error);
    }
  
    return data;
  };
export const deleteTrip = async (param: Record<string, string>={}) => {
  if (APP_MODE_DEV) {
    const { deleteTrip } = useMockupStore();
    return deleteTrip(Number(param.tripId));
  }
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
  if (APP_MODE_DEV) {
    const { addTrip } = useMockupStore();
    return addTrip(newTrip);
  }
    const { data, error } = await fetchData<NewTrip>(
      setParam(apiEndpoints.trip.create, param),
      { body: JSON.stringify({...newTrip,budget_amount:1}) },
      "POST"
    );
    if (error) {
      throw new Error(error);
    }
  
    return data;
  };

export const updateTrip = async (
    param: Record<string, string>,
    tripData: Partial<Trip>
) => {
  if (APP_MODE_DEV) {
    return {};
  }
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