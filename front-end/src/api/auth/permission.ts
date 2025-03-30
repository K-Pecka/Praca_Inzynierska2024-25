import { useMockupStore } from "@/mockup/useMockupStore";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchPermission = async () => {
  if (APP_MODE_DEV) {
    const { getUserProfile } = useMockupStore();
    const permission = getUserProfile();
<<<<<<< HEAD
    return permission.length==0? [1,2,3]:permission;
=======
    return permission.length==0?[1,2,3]: permission ;
>>>>>>> slave
  }
};