import { apiEndpoints, fetchData } from "@/api/apiEndpoints";

export const fetchLogOut = async () => {
  const { data, error } = await fetchData(apiEndpoints.auth.logout, "POST");

  if (error) {
    throw error;
  }

  return data;
};
