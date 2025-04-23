import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
  return new Validator(errorMessage).isEmpty().save();
};

export const loginInput = (errorMessage: Record<string, string>) => [
  {
    name: "email",
    label: "Podaj Email:",
    type: InputType.EMAIL,
    placeholder: "Wprowadź email",
    validation: getValidator(errorMessage),
    error: [],
  },
  {
    name: "password",
    label: "Podaj Hasło:",
    type: InputType.PASSWORD,
    placeholder: "Wprowadź hasło",
    validation: getValidator(errorMessage),
    error: [],
  },
];
export const getMoreOptions = () => [
    { label: "Zapomniałeś hasła?", href: {name:"home"} },
    { label: "Nie masz konta? Zarejestruj się.", href: {name:"register"} },
  ];
