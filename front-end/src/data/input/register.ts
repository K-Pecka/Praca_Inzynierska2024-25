import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).save();
};

export const registerInput = (errorMessage: Record<string, string>) => [
      {
        name: "first_name",
        label: "Podaj Imię:",
        type: InputType.TEXT,
        placeholder: "Wprowadź imię",
        validation: getValidator(errorMessage).minLength(3),
        config: { required: true },
        error: [],
      },
      {
        name: "last_name",
        label: "Podaj Nazwisko:",
        type: InputType.TEXT,
        placeholder: "Wprowadź nazwisko",
        validation: getValidator(errorMessage).minLength(3),
        config: { required: true },
        error: [],
      },
      {
        name: "email",
        label: "Podaj e-mail:",
        type: InputType.EMAIL,
        placeholder: "Wprowadź e-mail",
        validation: getValidator(errorMessage).email(),
        config: { required: true },
        error: [],
      },
      {
        name: "password",
        related: ["pass_2"],
        label: "Podaj hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź hasło",
        validation: getValidator(errorMessage).isEmpty().minLength(8).strongPassword(),
        config: { required: true },
        error: [],
      },
      {
        name: "pass_2",
        related: ["password"],
        label: "Podaj ponownie hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź hasło",
        validation: getValidator(errorMessage).isEmpty().minLength(8).strongPassword(),
        config: { required: true },
        error: [],
      }
    ];
