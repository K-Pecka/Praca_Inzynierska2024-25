import { Validator } from "@/utils/validator/validation";
import { NavigationFailure } from "vue-router";
import { TypeOfButton } from "./enum";
import { PricingPlanType } from "./types";

export interface TOKEN {
  refresh?: string;
  access?: string;
}
interface Config {
  required?: boolean;
  multiple?: boolean;
  min?: Date | string;
  max?: Date | string;
  edit?: boolean;
  maxDate?: Date | string;
  label?: string;
  maxLength?: number;
}

export interface Input {
  name: string;
  label: string;
  related?: string[];
  type: string;
  placeholder: string;
  validation: Validator | any; 
  config?: Config;
  error: string[];
}
export interface Register {
  email: String;
  first_name: String;
  last_name: String;
  date_of_birth: String;
  password: String;
}
export interface DashboardBox {
  title: string;
  icon?: string;
  content: string | string[] | BudgetData;
  set: {
    size: {
      sm?: { col: number; row: number };
      md?: { col: number; row: number };
      lg?: { col: number; row: number };
      xl?: { col: number; row: number };
    };
    order: number;
  };
  className?: string[];
}

export interface Button {
  type: TypeOfButton;
  title: string;
  class: String[];
  onclick: (id: string) => Promise<void> | void;
}
export interface Expense {
  id?: number;
  trip?: number;
  title: string;
  amount: number;
  currency: string;
  date: string;
  user: number;
  category: number;
  note?: string;
  username?: string;
  converted_amount?: string;
}
export interface ExpenseResponse{
  results:Expense[];
}
export interface TripData {
  results:Trip[];
}
export interface Trip {
  creator: { id: number; first_name: string;type: string; last_name: string };
  activity_for_today: number;
  activity_for_week: number;
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  country?: string;
  city?: string;
  members?: number[];
  pending_members?: Memebers[];
  activity_count?: number;
  budget_amount?: string;
  isOwner?: boolean;
}
export interface NewPlan {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  country?: string;
  city?: string;
  members?: number[];
  pending_members?: Memebers[];
  activity_count?: number;
  budget_amount?: string;
}
export interface Memebers {
  id: number;
  type: number;
  email: string;
}
export interface Budget {
  budget_amount: number;
}
export interface Btn {
  type: TypeOfButton;
  title: string;
  class: String[];
  onclick: (id: string) => Promise<void> | void;
}

export interface Phrase {
  word: string | string[];
  animation?: boolean;
  styles?: Record<string, string>;
}
export interface Link {
  href: { name: string } | string;
  label: string;
  className?: string[];
  active?: Boolean;
  style?: Record<string, string>;
}

export interface FooterData {
  links: Link[];
  footerText?: string;
  lastUpdated?: string;
}
export interface SubSectionData {
  title: string;
  items: {
    image: Image;
    caption: string;
  }[];
}
export interface SubSectionItem {
  image: Image;
  caption: string;
}

export interface SideNavItem {
  title: string;
  icon?: string;
  iconActive?: string;
  page?: { name: string };
  children?: { title: string; page: { name: string },isOwner?:boolean }[];
  permission?: number[];
  name?: string;
  isOwner?:boolean;
}

export interface FAQItem {
  question: string;
  answer: string;
}
export interface Image {
  img: string;
  alt: string;
  caption?: string;
}
export interface Role {
  type:string;
  title: string;
  description: string;
  image: Image;
  path: string | { name: string; params?: Record<string, string> };
}
export interface RoleSelection {
  title: string;
  subtitle: string;
  roles: Role[];
}

export interface NewTrip {
  name: string;
  start_date: string;
  end_date: string;
}
export interface Plan {
  activities_count? : number;
  id?: number;
  name: string;
  country: string;
  city?: string;
  start_date: string;
  end_date: string;
}
export interface PlanResponse{
  results:Plan[];
}
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

export interface PricingCard {
  type: PricingPlanType;
  name: string;
  price: string;
  features: string[];
  buttonVariant?: "primary" | "secondary";
  contentVariant?: "primary" | "secondary";
}
export interface InvateUser {
  id: string;
  email: string;
}

export interface BudgetData {
  amount: number;
  currency: string;
  expenses: number;
}
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
  ticekt?: string;
}
export interface ActivityResponse{
  results:Activity[];
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
  
}

export interface ActivityType {
  id: number;
  name: string;
}
export interface Profile {
  checkout_url: string;
  type: number;
  id: number;
  is_default: boolean;
}
export interface Debt {
  trip: number;
  name: string;
  amount: number;
  currency: string;
  members: number[];
}
export interface DebtDetails {
  id: number;
  creator:Profile
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
  results:DebtDetails[];
}
