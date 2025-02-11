import { defineStore } from "pinia";
import { Validator } from "@/utils/validator/validation";
import { usePageStore } from "@/stores/pageContentStore";
import {FormType,Input} from "@/type/interface";

export enum InputType {
  TEXT = "text",
  PASSWORD = "password",
  EMAIL = "email",
  DATE = "date"
}

export const useFormStore = defineStore("form", () => {
  const { errorMessage } = usePageStore();

  const getValidator = (errorMessage: () => Record<string, string>): Validator => {
    return new Validator(errorMessage()).isEmpty().save();
  };

  const getLoginInput = (): Input[] => [
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

  const getRegisterInput = (): Input[] => {
    const validator = new Validator({
      ...errorMessage(),
      isEqual: "Hasła muszą być takie same",
    }).save();

    return [
      {
        name: "first_name",
        label: "Podaj Imię:",
        type: InputType.TEXT,
        placeholder: "Wprowadź imię",
        validation: validator.createNew().minLength(3),
        config: { required: true },
        error: [],
      },
      {
        name: "last_name",
        label: "Podaj Nazwisko:",
        type: InputType.TEXT,
        placeholder: "Wprowadź nazwisko",
        validation: validator.createNew().minLength(3),
        config: { required: true },
        error: [],
      },
      {
        name: "email",
        label: "Podaj e-mail:",
        type: InputType.EMAIL,
        placeholder: "Wprowadź e-mail",
        validation: validator.createNew().email(),
        config: { required: true },
        error: [],
      },
      {
        name: "date_of_birth",
        label: "Data urodzenia:",
        type: InputType.DATE,
        placeholder: "Wprowadź date urodzenia",
        validation: validator,
        config: { required: true },
        error: [],
      },
      {
        name: "password",
        related: ["pass_2"],
        label: "Podaj hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź hasło",
        validation: validator.isEmpty(),
        config: { required: true },
        error: [],
      },
      {
        name: "pass_2",
        related: ["password"],
        label: "Podaj ponownie hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź hasło",
        validation: validator.isEmpty(),
        config: { required: true },
        error: [],
      },
    ];
  };

  const getPlanInput = (): Input[] => {
    const validator = new Validator({
      ...errorMessage(),
      dateRange: "Data zakończenia nie może być wcześniejsza niż rozpoczęcia",
    }).save();

    return [
      {
        name: "tripName",
        label: "Nazwa",
        type: "text",
        placeholder: "Zwiedzanie Paryża",
        validation: validator.createNew().isEmpty(),
        config: { required: true },
        error: [],
      },
      {
        name: "city",
        label: "Miasto",
        type: "text",
        placeholder: "np. Paryż",
        validation: validator.createNew().isEmpty(),
        config: { required: true },
        error: [],
      },
      {
        name: "tripDates",
        label: "Data podróży",
        type: "date",
        placeholder: "dd.mm.rrrr - dd.mm.rrrr",
        validation: validator.createNew().isEmpty(),
        config: { required: true },
        error: [],
      },

    ];
  };


  const getFormInputs = (type: FormType): Input[] => {
    if (type === FormType.LOGIN) return getLoginInput();
    if (type === FormType.REGISTER) return getRegisterInput();
    if (type === FormType.PLAN) return getPlanInput();

    return [];
  };

  const validateForm = (type: FormType, formValues: Record<string, string>) => {
    return getFormInputs(type).every((input) => {
      const value = formValues[input.name];
      const errors = input.validation ? input.validation.validate(value) : [];
      input.error = errors;
      return errors.length === 0;
    });
  };
  const getMoreOptions = () => [
    { label: "Zapomniałeś hasła?", href: "/" },
    { label: "Nie masz konta? Zarejestruj się.", href: "/register" },
  ]
  return { getFormInputs, validateForm, getMoreOptions };
});

