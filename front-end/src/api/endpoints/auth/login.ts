import apiClient from "@/api/apiClient";
import { apiEndpoints, backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";

export const loginFetch = async (credentials: Record<string, string>) => {
  try {
    const response = await apiClient.post(apiEndpoints.auth.login, credentials);
    if (response.status === 401 ){
      
      throw response.data || { message: "Unauthorized" };
    }
    return response.data;
  } catch (error: any) {
    const errorData = error.response?.data;
        throw errorData || { message: "unknown" };
  }
};
