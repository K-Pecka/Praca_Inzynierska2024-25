import { Validator } from "@/utils/validator/validation";

export enum FormType {
  LOGIN = "login",
  REGISTER = "register",
}

interface Config {
  required: boolean;
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