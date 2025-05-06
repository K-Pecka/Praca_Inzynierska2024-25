import { Validator } from "@/utils/validator/validation";
import { NavigationFailure } from "vue-router";
import { TypeOfButton } from "./enum";

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
}

export interface Input {
  name: string;
  label: string;
  related?: string[];
  type: string;
  placeholder: string;
  validation: Validator | any; //TODO: naprawić użycie any<tymczasowo>
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
  trip?: number;
  title: string;
  amount: number;
  currency: string;
  date: string;
  user: number;
  category: number;
  note?: string;
}
export interface Trip {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  country?: string;
  city?: string;
  members?: number[];
  budget?: Budget;
  pending_members?: Memebers[];
}
export interface Memebers {
  id: number;
  type: number;
  email: string;
}
export interface Budget {
  amount: string;
  currency: string;
  trip: number;
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
  label: string;
  icon?: string;
  iconActive?: string;
  route?: string | { name: string; params?: Record<string, string> };
  children?: SideNavItem[];
  permission?: number[];
  name?: string;
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
  title: String;
  description: String;
  image: Image;
  path: string | { name: string; params?: Record<string, string> };
}
export interface RoleSelection {
  title: String;
  subtitle: String;
  roles: Role[];
}

export interface NewTrip {
  name: string;
  start_date: string;
  end_date: string;
}
export interface Plan {
  id: number;
  name: string;
  country: string;
  city?: string;
  start_date: string;
  end_date: string;
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
  profile: number;
  valid_from_date: string;
  valid_from_time: string;
  trip: number;
  type_display?: string;
}

export interface PricingCard {
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
  convertedAmount: number;
  convertedCurrency: string;
  expenses: number;
}
export interface Activity {
  id: number;
  type: string;
  name: string;
  date: string;
  start_time?: string;
  duration?: string;
  location?: string;
  assignedTo?: string;
  description?: string;
}
export interface User {
  userId: number;
  first_name?: string;
  last_name?: string;
  email?: string;
  name?: string;
  is_guest?: boolean;
}
