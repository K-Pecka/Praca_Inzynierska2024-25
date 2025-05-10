import { apiEndpoints, fetchData } from "@/api/apiEndpoints";

export const fetchPermission = async () => {
  try {
    const { data, error } = await fetchData(
      apiEndpoints.auth.profile,
      {},
      "GET"
    );

    if (error) {
      throw new Error(error);
    }

    return data || [1, 2, 3];
  } catch (error) {
    return [1, 2, 3];
  }
};
