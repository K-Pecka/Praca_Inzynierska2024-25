import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { Ticket, NewTrip } from "@/types/interface";

export const createTicket = async (
  ticket: Ticket,
  body: Record<string, string>={},
  param: Record<string, string> = {}
) => {
  const { data, error } = await fetchData<Ticket>(
    setParam(apiEndpoints.plan.create, param),
    { body: JSON.stringify(ticket) },
    "POST"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};
