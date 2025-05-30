import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";
import { max } from "moment";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const tripInput = (errorMessage: Record<string, string>) => [
      {
        name: "tripName",
        label: "Nazwa",
        type: InputType.TEXT,
        placeholder: "Podaj nazwę wycieczki",
        validation: getValidator(errorMessage).maxLength(50),
        config: { required: true,maxLength:50 },
        error: [],
      },
      {
        name: "tripDates",
        label: "Termin wycieczki",
        type: InputType.DATE_RANGE,
        placeholder: "dd.mm.rrrr - dd.mm.rrrr",
        validation: getValidator(errorMessage),
        config: { required: true, multiple: true,min: new Date(new Date().setDate(new Date().getDate() - 1)) },
        error: [],
      },
    ];
