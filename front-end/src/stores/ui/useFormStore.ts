import { defineStore } from "pinia";
import { usePageStore } from "@/stores/pageContentStore";
import { FormType, Input } from "@/type/interface";
import {
  loginInput,
  registerInput,
  planInput,
  tripInput,
  budgetInput,
  getMoreOptions,
} from "@/dataStorage/index";

export const useFormStore = defineStore("form", () => {
  const { errorMessage } = usePageStore();
  const extraValidationMessages = {
    isEqual: "Hasła muszą być takie same",
    dateRange: "Data zakończenia nie może być wcześniejsza niż rozpoczęcia",
  };
  const getLoginInputs = (): Input[] => loginInput(errorMessage());

  const getRegisterInputs = (): Input[] =>
    registerInput(errorMessage({ isEqual: extraValidationMessages.isEqual }));

  const getPlanInputs = (): Input[] =>
    planInput(errorMessage({ dateRange: extraValidationMessages.dateRange }));

  const getTripInputs = (): Input[] =>
    tripInput(errorMessage({ dateRange: extraValidationMessages.dateRange }));

  const getBudgetInputs = (): Input[] => budgetInput(errorMessage());

  const formInputGenerators: Record<FormType, () => Input[]> = {
    [FormType.LOGIN]: getLoginInputs,
    [FormType.REGISTER]: getRegisterInputs,
    [FormType.PLAN]: getPlanInputs,
    [FormType.TRIP]: getTripInputs,
    [FormType.BUDGET]: getBudgetInputs,
  };
  const getFormInputs = (type: FormType): Input[] =>
    formInputGenerators[type]?.() ?? [];

  const isFormValid  = (type: FormType, formValues: Record<string, string>) => {
    return getFormInputs(type).every((input) => {
      const value = formValues[input.name];
      let errors: string[] = [];

      if (input.validation && "validate" in input.validation) {
        errors = input.validation.validate(value);
      }

      input.error = errors;
      return errors.length === 0;
    });
  };
  return { getFormInputs, isFormValid, getMoreOptions };
});
