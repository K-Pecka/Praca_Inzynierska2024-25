import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { APP_MODE_DEV } from "@/config/envParams";
import { Activity, ActivityType } from "@/types";
export const createActivity = async (newActivity:Activity,param: Record<string, string>={}) => {
  if (APP_MODE_DEV) {
    return {};
  }
    const { data, error } = await fetchData<Activity>(
      setParam(apiEndpoints.activity.create, param),
      { body: JSON.stringify({...newActivity}) },
      "POST"
    );
    if (error) {
      throw new Error(error);
    }
  
    return data;
  };
  export const fetchActivity = async (param: Record<string, string> = {}):Promise<Activity[]> => {
    if (APP_MODE_DEV) {
      return [];
    }
    const { data, error } = await fetchData<Activity>(
      setParam(apiEndpoints.activity.all, param),
      {},
      "GET"
    );
    if (error) {
      throw new Error(error);
    }
  
    return Array.isArray(data) ? data : [];
  }

export const fetchActivityTypes = async (tripId: string): Promise<ActivityType[]> => {
  const url = setParam(apiEndpoints.activityType.all, { tripId });
  const { data, error } = await fetchData<ActivityType[]>(url);

  if (error) {
    throw new Error(error);
  }

  return data || [];
};