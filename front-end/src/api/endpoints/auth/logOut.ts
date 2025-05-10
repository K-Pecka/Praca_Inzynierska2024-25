import {
  apiEndpoints,
  fetchData,
  standardHeaders,
} from "@/api/apiEndpoints";

export const fetchLogOut = async () => {
  const { data, error } = await fetchData(
      apiEndpoints.auth.logout,
      {
        headers: standardHeaders(),
      },
      "POST"
  );

  if (error) {
    throw new Error(error);
  }

  return data;
};
