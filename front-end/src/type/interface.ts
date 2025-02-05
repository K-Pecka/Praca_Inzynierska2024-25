import { Validator } from "@/utils/validator/validation";

export interface Input {
    name: string;
    label: string;
    type: string;
    placeholder: string;
    validation: Validator;
    error: string[];
  }