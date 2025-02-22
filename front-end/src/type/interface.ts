import { Validator } from "@/utils/validator/validation";

export interface TOKEN {
  refresh: string;
  access: string;
}
interface Config {
  required?: boolean;
  multiple?:boolean;
}

export interface Input {
    name: string;
    label: string;
    related?:string[],
    type: string;
    placeholder: string;
    validation: Validator | any; //TODO: naprawić użycie any<tymczasowo>
    config?:Config,
    error: string[];
  }
export interface Register{
    email: String,
    first_name: String,
    last_name: String,
    date_of_birth: String,
    password: String
  }
export interface DashboardBox {
  title: string;
  content: string | string[];
  set: {
    size: {
      sm?: { col: number; row: number };
      md?: { col: number; row: number };
      lg?: { col: number; row: number };
      xl?: { col: number; row: number };
    };
    order: number;
  };
}

export interface Button {
  title: string;
  class: String[];
  onclick: (id: number) => void;
}

export interface Trip {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
}

export interface Btn {
  actions: {
    title: string;
    class: String[];
    onclick: (id: Number) => void;
  }[];
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
    image: string;
    alt: string;
    caption: string;
  }[];
}
export interface SubSectionItem {
  image: string;
  alt: string;
  caption: string;
}

export interface SideNavItem {
  label: string;
  icon?: string;
  iconActive?: string;
  route?: string | {name:string,params?:Record<string,string>};
  children?: SideNavItem[];
}

export interface FAQItem {
  question: string;
  answer: string;
}

export interface Role{
  title: String,
  description: String,
  image: string,
  path: string | { name: string; params?: Record<string, string> };
}
export interface RoleSelection{
  title: String,
  subtitle: String,
  roles: Role[]
}