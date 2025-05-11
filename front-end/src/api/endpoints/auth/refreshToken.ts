import apiClient from "@/api/apiClient";
import { TOKEN } from "@/types/interface";
import { apiEndpoints } from "@/api/apiEndpoints";

export const fetchRefreshToken = async (token: TOKEN) => {
  try {
    const response = await apiClient.post(apiEndpoints.auth.refreshToken, {
      refresh: token.refresh,
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