import { apiEndpoints, fetchData, setParam } from "@/api/apiEndpoints";
import { User } from "@/types";

export const fetchUserById = async (id: number) => {
  const url = setParam(apiEndpoints.user.getUserById, { userId: id.toString() });

  const { data, error } = await fetchData<User>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data as User;
};