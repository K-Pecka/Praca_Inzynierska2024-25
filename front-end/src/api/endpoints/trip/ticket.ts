import apiClient from "@/api/apiClient";
import { apiEndpoints, fetchData, setParam } from "../../apiEndpoints";
import { TicketData, TicketResponse } from "@/types/interface";

export const fetchTicket = async (params: { [key: string]: string }) => {
  const url = setParam(apiEndpoints.ticket.all, params);

  const { data, error } = await fetchData<TicketResponse>(url, "GET");

  if (error) {
    throw error;
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
) => {
  const url = setParam(apiEndpoints.ticket.delete, params);
  const { data, error } = await fetchData(url, "DELETE");
  if (error) {
    throw error;
  }
  return params;
};
export const updateMembers = async (
  newMembers:number[],
  params: Record<string, string>
) => {
  const url = setParam(apiEndpoints.ticket.updateMembers, params);
  const formData = new FormData();
  newMembers.forEach((id) => {
      formData.append("profiles", String(id));
    });
  try {
    const response = await apiClient.patch(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error: any) {
    throw new Error("Błąd podczas tworzenia biletu");
  }
};