import { Validator } from "@/utils/validator/validation";

export enum FormType {
  LOGIN = "login",
  REGISTER = "register",
  PLAN = "plan",
}

interface Config {
  required?: boolean;
  multiple?:true;
}
export interface Input {
    name: string;
    label: string;
    related?:string[],
    type: string;
    placeholder: string;
    validation: Validator;
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