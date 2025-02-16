import { Validator } from "@/utils/validator/validation";

export enum FormType {
  LOGIN = "login",
  REGISTER = "register",
  PLAN = "plan",
  TRIP = "trip",
  BUDGET = "budget"
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