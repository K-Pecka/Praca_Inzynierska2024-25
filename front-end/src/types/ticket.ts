export interface Ticket {
  id: string;
  type: string;
  name: string;
  date: string;
  assignedTo?: string | string[];
  file?: File;
}

export interface TicketData {
  id: number;
  name: string;
  file: string;
  type: string;
  profiles: number[];
  valid_from_date: string;
  valid_from_time: string;
  trip: number;
  type_display?: string;
}

export interface TicketResponse {
  results: TicketData[];
}
