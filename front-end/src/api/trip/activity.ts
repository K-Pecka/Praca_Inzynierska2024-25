import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { APP_MODE_DEV } from "@/config/envParams";
import { Activity } from "@/type";
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
