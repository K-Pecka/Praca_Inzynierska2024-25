import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Activity, ActivityType } from "@/types";

export const createActivity = async (newActivity: Activity, param: Record<string, string> = {}) => {
    const url = setParam(apiEndpoints.activity.create, param);

    const { data, error } = await fetchData<Activity>(url, "POST", newActivity);

    if (error) {
        throw new Error(error);
    }

    return data;
};


export const fetchActivity = async (param: Record<string, string> = {}): Promise<Activity[]> => {
    const url = setParam(apiEndpoints.activity.all, param);

    const { data, error } = await fetchData<Activity[]>(url, "GET");

    if (error) {
        throw new Error(error);
    }

    return Array.isArray(data) ? data : [];
};


export const fetchActivityDelete = async (param: Record<string, string> = {}) => {
    
    const url = setParam(apiEndpoints.activity.delete, param);
    const { error } = await fetchData(url, "DELETE");

    if (error) {
        throw new Error(error);
    }

    return param;
};


export const fetchActivityTypes = async (tripId: string): Promise<ActivityType[]> => {
    const url = setParam(apiEndpoints.activityType.all, { tripId });

    const { data, error } = await fetchData<ActivityType[]>(url, "GET");

    if (error) {
        throw new Error(error);
    }

    return data || [];
};