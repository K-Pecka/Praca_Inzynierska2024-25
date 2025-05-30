export interface Activity {
  id: number;
  type: number;
  name: string;
  date: string;
  start_time?: string;
  duration?: string;
  location?: string;
  assignedTo?: string;
  description?: string;
  ticket?: string;
}

export interface ActivityResponse {
  results: Activity[];
}

export interface ActivityType {
  id: number;
  name: string;
}
