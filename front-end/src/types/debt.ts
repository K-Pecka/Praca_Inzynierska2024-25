import type { Profile } from './auth';

export interface Debt {
  trip: number;
  name: string;
  amount: number;
  currency: string;
  members: number[];
}

export interface DebtDetails {
  id: number;
  creator: Profile;
  name: string;
  amount: string;
  currency: string;
  amount_in_pln: string;
  members: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  }[];
  amount_per_member: string;
  amount_per_member_in_pln: string;
}

export interface DebtResponse {
  results: DebtDetails[];
}
