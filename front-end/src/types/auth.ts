export interface TOKEN {
  refresh?: string;
  access?: string;
  initialAccessToken?: string;
}

export interface Register {
  email: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  password: string;
}

export interface User {
  userId: number;
  first_name?: string;
  last_name?: string;
  email?: string;
  name?: string | null;
  is_guest?: boolean;
  is_owner?: boolean;
  profiles?: Profile[];
  fullname?: string;
  subscription_active?: boolean;
  subscription_plan?: string;
  subscription_cancelled?: boolean;
}

export interface Profile {
  checkout_url: string;
  type: number;
  id: number;
  is_default: boolean;
}
