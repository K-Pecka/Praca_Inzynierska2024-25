import apiClient from "@/api/apiClient";
import { TOKEN } from "@/types/interface";
import { apiEndpoints, backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";
import { APP_MODE_DEV } from "@/config/envParams";

export const fetchRefreshToken = async (token: TOKEN) => {
  if (APP_MODE_DEV) {
    return { access: token.access, refresh: token.refresh };
  }

  try {
    const response = await apiClient.post(apiEndpoints.auth.refreshToken, {
      refresh: token.refresh,
    });

    return response.data;
  } catch (error: any) {
    let errorData = null;
    if (backendNotification && error.response?.data) {
      errorData = error.response.data;
    }
    const { tokenError } = useNotificationStore();
    throw new Error(errorData || tokenError());
  }
};