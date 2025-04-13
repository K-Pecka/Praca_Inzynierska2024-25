import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { APP_MODE_DEV } from "@/config/envParams";
import { useMockupStore } from "@/mockup/useMockupStore";
export interface Activity {
    id: string;
    type: string;
    name: string;
    date: string;
    startTime: string;
    duration: string;
    location?: string;
    assignedTo?: string;
    description?: string;
}
export const createActivity = async (newActivity:Activity,param: Record<string, string>={}) => {
  if (APP_MODE_DEV) {
    const { addTrip } = useMockupStore();
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
