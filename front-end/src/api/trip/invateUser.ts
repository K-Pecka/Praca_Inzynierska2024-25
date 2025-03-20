import { Exception } from "sass";
import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Ticket, InvateUser } from "@/type/interface";

export const invateUser = async (
  userEmail: string,
  param: Record<string, string> = {}
) => {
  const { data: userId, error: errorUser } = await fetchData<InvateUser[]>(
    setParam(`${apiEndpoints.auth.profile}?email=${userEmail}`, param),
    {},
    "GET"
  );
  if (errorUser || !userId) throw new Error(errorUser);
  param = {...param,userId:userId[0].id};
  console.log(setParam(`${apiEndpoints.trip.invateUser}?action=add`, param),);
  const { data, error } = await fetchData<InvateUser[]>(
    setParam(`${apiEndpoints.trip.invateUser}?action=add`, param),
    {},
    "PATCH"
  );
  if (error) {
    return;
  }

  return data;
};
