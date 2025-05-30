import apiClient from "@/api/apiClient";
import { apiEndpoints } from "@/api/apiEndpoints";

export const fetchRefreshToken = async (refresh: string) => {
  try {
    const response = await apiClient.post(apiEndpoints.auth.refreshToken, {
      refresh: refresh,
    });

    return response.data;
  } catch (error: any) {
    const message =
        error.response?.data?.message ||
        error.message ||
        "Nie udało się odświeżyć tokena";

    throw new Error(message);
  }
};