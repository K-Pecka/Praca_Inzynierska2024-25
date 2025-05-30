import type { Validator } from '@/utils/validator/validation';
import type { TypeOfButton } from './enum';
import type { BudgetData } from './budget';

export interface InputConfig {
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
  config?: InputConfig;
  error: string[];
}

export interface Button {
  type: TypeOfButton;
  title: string;
  class: string[];
  onclick: (id: string) => Promise<void> | void;
}

export interface Btn {
  type: TypeOfButton;
  title: string;
  class: string[];
  onclick: (id: string) => Promise<void> | void;
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

export interface Phrase {
  word: string | string[];
  animation?: boolean;
  styles?: Record<string, string>;
}

export interface Link {
  href: { name: string } | string;
  label: string;
  className?: string[];
  active?: boolean;
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
  children?: { title: string; page: { name: string }; isOwner?: boolean; activeSubscription?: boolean }[];
  permission?: number[];
  name?: string;
  isOwner?: boolean;
  activeSubscription?: boolean;
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
