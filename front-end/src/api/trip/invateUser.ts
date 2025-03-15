import { apiEndpoints, fetchData, setParam } from "../apiEndpoints";
import { Ticket, InvateUser } from "@/type/interface";

export const invateUser = async (
  idUser: number,
  param: Record<string, string> = {}
) => {
  const { data, error } = await fetchData<InvateUser[]>(
    setParam(apiEndpoints.plan.create, param),
    {},
    "POST"
  );
  if (error) {
    return;
  }

  return data;
};
