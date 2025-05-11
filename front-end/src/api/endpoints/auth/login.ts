import apiClient from "@/api/apiClient";
import { apiEndpoints, backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";

export const loginFetch = async (credentials: Record<string, string>) => {
  try {
    const response = await apiClient.post(apiEndpoints.auth.login, credentials);
    return response.data;
  } catch (error: any) {
    let errorData = null;
    if (backendNotification && error.response?.data) {
      errorData = error.response.data;
    }
    const { loginError } = useNotificationStore();
    throw new Error(errorData || loginError());
  }
};
