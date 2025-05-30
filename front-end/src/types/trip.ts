export interface Trip {
  creator: { id: number; first_name: string; type: string; last_name: string };
  activity_for_today: number;
  activity_for_week: number;
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  country?: string;
  city?: string;
  members?: number[];
  pending_members?: Member[];
  activity_count?: number;
  budget_amount?: string;
  isOwner?: boolean;
}

export interface TripData {
  results: Trip[];
  count: number;
}

export interface NewTrip {
  name: string;
  start_date: string;
  end_date: string;
}

export interface Itinerary{
  activities_count?: number;
  id?: number;
  name: string;
  country: string;
  city?: string;
  start_date: string;
  end_date: string;
}

export interface ItineraryResponse {
  results: Itinerary[];
}

export interface Member {
  id: number;
  type: number;
  email: string;
}
export interface NewItinerary {
  id?: number;
  name: string;
  start_date: string;
  end_date: string;
  country?: string;
  city?: string;
  members?: number[];
  pending_members?: Member[];
  activity_count?: number;
  budget_amount?: string;
}