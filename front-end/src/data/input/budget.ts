import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const budgetInput = (errorMessage: Record<string, string>) => [
      {
        name: "amount",
        label: "Kwota:",
        type: InputType.TEXT,
        placeholder: "np. 6000",
        validation: getValidator(errorMessage).minValue(0),
        error: [],
      },
      {
        name: "currency",
        label: "Waluta:",
        type: InputType.TEXT,
        placeholder: "PLN",
        validation: getValidator(errorMessage).isEmpty(),
        error: [],
      },
    ];
