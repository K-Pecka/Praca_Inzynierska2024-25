import { useAuthStore } from "@/stores";
import { invateUser } from "./trip";
export const hostName = "https://api.plannder.com";
export const backendNotification = false;
export const standardHeaders = () => {
  const { getToken } = useAuthStore();
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${getToken()?.access}`,
  };
};
let notificationTimeout: ReturnType<typeof setTimeout> | null = null;
export const fetchData = async <T = unknown>(
  url: string,
  options: RequestInit = { body: undefined },
  method: "GET" | "POST" | "DELETE" | "PATCH" | "PUT" = "GET"
): Promise<{ data?: T; error?: string }> => {
  if(notificationTimeout) 
    return {error:"Jestem w trakcie wykonania\n poprzedniego zapytania..."};
  notificationTimeout = setTimeout(() => {
    notificationTimeout = null;
  }, 3000);
  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        ...standardHeaders(),
      },
      ...options,
      body: options.body ? options.body : undefined,
    });

    const result = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(result?.message || `Błąd HTTP: ${response.status}`);
    }
    return { data: result };
  } catch (error: any) {
    return { error: error.message || "Wystąpił błąd" };
  }
};
export const setParam = (url: string, params: Record<string, string>): string => {
  return Object.keys(params).reduce((acc, key) => {
    if (acc.includes(`:${key}`)) {
      return acc.replace(`:${key}`, encodeURIComponent(params[key]));
    } else {
      console.warn(`Missing parameter: ${key}`);
      return acc;
    }
  }, url);
};
  
export const apiEndpoints = {
  auth: {
    login: `${hostName}/user_auth/login/`,
    register: `${hostName}/user/create/`,
    refreshToken: `${hostName}/user_auth/token/refresh/`,
    verify: `${hostName}/user_auth/token/verify/`,
    profile: `${hostName}/user/profile/`,
    logout: `${hostName}/user_auth/logout/`,
  },
  trip: {
    all: `${hostName}/trip/all/`,
    detail: `${hostName}/trip/:tripId/`,
    delete: `${hostName}/trip/:tripId/delete/`,
    create: `${hostName}/trip/create/`,
    update: `${hostName}/trip/:tripId/update/`,
    invateUser: `${hostName}/trip/:tripId/participants/manage/:userId/`
  },
  plan: {
    all: `${hostName}/trip/:tripId/itinerary/`,
    detail: `${hostName}/trip/:tripId/itinerary/:planId/`,
    delete: `${hostName}/trip/:tripId/itinerary/:planId/delete/`,
    create: `${hostName}/trip/:tripId/itinerary/create/`,
  },
  ticket:{
    create:`${hostName}/trip/ticket/create/`
  },
  budget: {
    update: `${hostName}/trip/:tripId/budget/update/`,
}
};
