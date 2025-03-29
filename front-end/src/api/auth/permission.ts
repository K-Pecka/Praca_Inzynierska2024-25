import { useMockupStore } from "@/mockup/useMockupStore";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchPermission = async () => {
  if (APP_MODE_DEV) {
    const { getUserProfile } = useMockupStore();
    return getUserProfile();
  }
};