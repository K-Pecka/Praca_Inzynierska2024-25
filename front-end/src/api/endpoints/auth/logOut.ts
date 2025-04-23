import {
  apiEndpoints,
  fetchData,
} from "@/api/apiEndpoints";
import { useMockupStore } from "@/mockup/useMockupStore";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchLogOut = async () => {
  if (APP_MODE_DEV) {
      const { logOut } = useMockupStore();
      return logOut();
    }
  const { data, error } = await fetchData(
    apiEndpoints.auth.logout,
    {},
    "POST"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
