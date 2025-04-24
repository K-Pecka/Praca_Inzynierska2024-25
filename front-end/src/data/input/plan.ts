import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const planInput = (errorMessage: Record<string, string>) => [
      {
        name: "tripName",
        label: "Nazwa",
        type: "text",
        placeholder: "Zwiedzanie Paryża",
        validation: getValidator(errorMessage),
        config: { required: true },
        error: [],
      },
      {
        name: "city",
        label: "Miasto",
        type: InputType.TEXT,
        placeholder: "np. Paryż",
        validation: getValidator(errorMessage),
        config: { required: true },
        error: [],
      },
      {
        name: "tripDates",
        label: "Data podróży",
        type: InputType.DATE_RANGE,
        placeholder: "dd.mm.rrrr - dd.mm.rrrr",
        validation: getValidator(errorMessage).isEmpty(),
        config: { required: true, multiple:true },
        error: [],
      }
    ];
