import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Trip,NewTrip } from "@/type/interface";
export const fetchTrips = async () => {
  const { data, error } = await fetchData<Trip[]>(
    apiEndpoints.trip.all,
    {},
    "GET"
  );
  console.log(data);
  if (error) {
    console.error("Błąd pobierania podróży:", error);
    return [];
  }
  if(!data){
    console.error("Błąd pobierania podróży:", data);
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
    console.log(data);
    if (error) {
      console.error("Błąd pobierania podróży:", error);
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
  console.log(setParam(apiEndpoints.trip.delete, param));
  if (error) {
    console.error("Błąd pobierania podróży:", error);
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
    console.log(setParam(apiEndpoints.plan.create, param));
    if (error) {
      console.error("Błąd pobierania podróży:", error);
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
        console.error("Błąd aktualizacji wycieczki:", error);
        throw new Error(error);
    }
    return data;
};