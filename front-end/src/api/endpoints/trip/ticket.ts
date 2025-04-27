import { apiEndpoints, fetchData, standardHeaders } from "../../apiEndpoints";
import { Ticket, TicketData } from "@/types/interface";

export const fetchTicket = async () => {
  
  const { data, error } = await fetchData<TicketData[]>(
    apiEndpoints.ticket.all,
    {},
    "GET"
  );
  if (error) {
    throw new Error(error);
  }

  return data;
};

export const createTicket = async (
  formData: FormData,
): Promise<any> => {
  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });
  const response = await fetch(apiEndpoints.ticket.create, {
    method: 'POST',
    headers: {
      ...standardHeaders(),
      
    },
    body: formData,
  });
  console.log('Response:', {
    method: 'POST',
    headers: {
      ...standardHeaders(),
      'Content-Type': 'multipart/form-data',
    },
    body: formData,
  });
  if (!response.ok) {
    console.error('Error response:', response.json());
    throw new Error('Błąd podczas tworzenia biletu');
  }

  return await response.json();
};