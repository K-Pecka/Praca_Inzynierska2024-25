import { apiEndpoints,backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";
export const loginFetch = async (credentials: Record<string, string>) => {
  const response = await fetch(apiEndpoints.auth.login, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  if (!response.ok) {
    let errorData = null;
    if(backendNotification){
      errorData = await response.json();
    }
    const {loginError} = useNotificationStore();
    throw new Error(errorData || loginError());
  }
  return response.json();
};
