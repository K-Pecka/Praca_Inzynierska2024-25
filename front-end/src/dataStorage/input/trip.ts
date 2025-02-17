import { InputType } from "@/type/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const tripInput = (errorMessage: Record<string, string>) => [
      {
        name: "tripName",
        label: "Nazwa",
        type: InputType.TEXT,
        placeholder: "Bałkany",
        validation: getValidator(errorMessage),
        config: { required: true },
        error: [],
      },
      {
        name: "tripDates",
        label: "Data wycieczki",
        type: InputType.DATE_RANGE,
        placeholder: "dd.mm.rrrr - dd.mm.rrrr",
        validation: getValidator(errorMessage),
        config: { required: true, multiple: true },
        error: [],
      },
    ];
