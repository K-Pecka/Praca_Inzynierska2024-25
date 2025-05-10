import { useAuthStore } from "@/stores";
import { apiEndpoints, fetchData, setParam, standardHeaders } from "../../apiEndpoints";
import { Ticket, TicketData } from "@/types/interface";

export const fetchTicket = async (params: { [key: string]: string }) => {
  
  const { data, error } = await fetchData<TicketData[]>(
    setParam(apiEndpoints.ticket.all,params),
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};

export const createTicket = async (
  formData: FormData,params: Record<string, string>
): Promise<any> => {
  formData.forEach((value, key) => {
  });
  const { getToken } = useAuthStore();
  const response = await fetch(setParam(apiEndpoints.ticket.create,params), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${getToken()?.access}`
    },
    body: formData,
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error('Błąd podczas tworzenia biletu');
  }

  return await response.json();
};

export const deleteTicket = async (
    params: Record<string, string>
): Promise<void> => {
  const { getToken } = useAuthStore();

  const response = await fetch(setParam(apiEndpoints.ticket.delete, params), {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${getToken()?.access}`
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error("Błąd podczas usuwania biletu");
  }
};