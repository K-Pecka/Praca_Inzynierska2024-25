import { apiEndpoints,backendNotification } from "@/api/apiEndpoints";
import { useNotificationStore } from "@/stores";
import { useMockupStore } from "@/mockup/useMockupStore";
import { APP_MODE_DEV } from "@/config/envParams";
export const loginFetch = async (credentials: Record<string, string>) => {
  if (APP_MODE_DEV) {
    console.log(credentials)
    const { login } = useMockupStore();
    return login(credentials.email, credentials.password);
  }
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