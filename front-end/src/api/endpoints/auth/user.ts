
import { apiEndpoints,fetchData,setParam } from "@/api/apiEndpoints";
import {User} from "@/types"
export const fetchUserById = async (id:number) => {
  const { data, error } = await fetchData<User>(
      setParam(apiEndpoints.user.getUserById,{ userId: id.toString() }),
      { },
      "GET"
    );
    if (error) {
      throw new Error(error);
    }

    return data as User;
  };