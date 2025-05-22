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
export const updateUser = async (dto: { first_name?: string; last_name?: string;  password?: string; password_confirm?: string }) => {

  const { data, error } = await fetchData<User>(apiEndpoints.user.update, "PATCH",dto);

  if (error) {
    throw new Error(error);
  }

  return data as User;
};
export const fetchUserRole = async (role: string) => {
  const url = setParam(apiEndpoints.user.role, { role });
  console.log("Fetching user role:", url);
  const { data, error } = await fetchData<User>(url, "PATCH");

  if (error) {
    throw new Error(error);
  }

  return data as User;
};