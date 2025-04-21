import { TOKEN } from "@/type/interface";
import { apiEndpoints, backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchRefreshToken = async (token: TOKEN) => {
  if (APP_MODE_DEV) {
    return {access:token.access,refresh:token.refresh};
  }
  const response = await fetch(apiEndpoints.auth.refreshToken, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: token.refresh }),
  });
  if (!response.ok) {
    let errorData = null;
    if (backendNotification) {
      errorData = await response.json();
    }
    const { tokenError } = useNotificationStore();
    throw new Error(errorData || tokenError());
  }

  return response.json();
};
