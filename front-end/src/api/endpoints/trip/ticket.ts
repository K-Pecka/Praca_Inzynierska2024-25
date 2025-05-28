import apiClient from "@/api/apiClient";
import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { TicketData,TicketResponse } from "@/types/interface";

export const fetchTicket = async (params: { [key: string]: string }) => {
  const url = setParam(apiEndpoints.ticket.all, params);

  const { data, error } = await fetchData<TicketResponse>(url, "GET");

  if (error) {
    throw new Error(error);
  }

  return data?.results;
};

export const createTicket = async (
    formData: FormData,
    params: Record<string, string>
): Promise<any> => {
  const url = setParam(apiEndpoints.ticket.create, params);

  try {
    const response = await apiClient.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error: any) {
    throw new Error("Błąd podczas tworzenia biletu");
  }
};

export const deleteTicket = async (
    params: Record<string, string>
): Promise<void> => {
  const url = setParam(apiEndpoints.ticket.delete, params);

  try {
    await apiClient.delete(url);
  } catch (error: any) {
    throw new Error("Błąd podczas usuwania biletu");
  }
};