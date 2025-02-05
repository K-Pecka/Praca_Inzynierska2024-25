// formStore.ts
import { defineStore } from "pinia";
import { Validator } from "@/utils/validator/validation";
import { Input } from "@/type/interface";
import { usePageStore } from "@/stores/pageContentStore";

export const useFormStore = defineStore("form", () => {
  const { errorMessage } = usePageStore();

  // Stwórz instancję Validatora, aby była bardziej elastyczna
  const getValidator = (errorMessage: () => Record<string, string>): Validator => {
    return new Validator(errorMessage()).isEmpty().save();
  };

  const getLoginInput = (): Input[] => {
    return [
      {
        name: "email",
        label: "Podaj Email:",
        type: "text",
        placeholder: "Wprowadź email",
        validation: getValidator(errorMessage),
        error: [],
      },
      {
        name: "password",
        label: "Podaj Hasło:",
        type: "password",
        placeholder: "Wprowadź hasło",
        validation: getValidator(errorMessage),
        error: [],
      },
    ];
  };
  const getMoreOptions = () => [
    { label: "Zapomniałeś hasła?", href: "/" },
    { label: "Nie masz konta? Zarejestruj się.", href: "/register" },
  ]
  const validateForm = (
    inputs: Input[],
    formValues: Record<string, string>
  ) => {
    return inputs.every((input) => {
      const value = formValues[input.name];
      const errors = input.validation ? input.validation.validate(value) : [];
      input.error = errors;
      return errors.length === 0;
    });
  };

  return { getLoginInput, validateForm,getMoreOptions };
});
