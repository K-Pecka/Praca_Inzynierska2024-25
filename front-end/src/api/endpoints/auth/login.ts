import apiClient from "@/api/apiClient";
import { apiEndpoints } from "@/api/apiEndpoints";

export const loginFetch = async (credentials: Record<string, string>) => {
  try {
    const response = await apiClient.post(apiEndpoints.auth.login, credentials);
    return response.data;
  } catch (error: any) {
    const errorData = error.response?.data;
        throw errorData || { message: "unknown" };
  }
};
