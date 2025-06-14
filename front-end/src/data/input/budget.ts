import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const budgetInput = (errorMessage: Record<string, string>) => [
      {
        name: "budget_amount",
        label: "Kwota",
        type: InputType.TEXT,
        placeholder: "np. 6000",
        validation: getValidator(errorMessage).minValue(0),
        error: [],
      }
    ];
