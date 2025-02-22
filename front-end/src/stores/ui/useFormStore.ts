import { defineStore } from "pinia";
import { useNotificationStore } from "@/stores/ui/useNotificationStore";
import { Input } from "@/type/interface";
import { FormType } from "@/type/enum";
import {
  loginInput,
  registerInput,
  planInput,
  tripInput,
  budgetInput,
  getMoreOptions,
} from "@/dataStorage/index";

export const useFormStore = defineStore("form", () => {
  const { getErrorMessages } = useNotificationStore();
  const extraValidationMessages = {
    isEqual: "Hasła muszą być takie same",
    dateRange: "Data zakończenia nie może być wcześniejsza niż rozpoczęcia",
  };
  const getLoginInputs = (): Input[] => loginInput(getErrorMessages());

  const getRegisterInputs = (): Input[] =>
    registerInput(getErrorMessages({ isEqual: extraValidationMessages.isEqual }));

  const getPlanInputs = (): Input[] =>
    planInput(getErrorMessages({ dateRange: extraValidationMessages.dateRange }));

  const getTripInputs = (): Input[] =>
    tripInput(getErrorMessages({ dateRange: extraValidationMessages.dateRange }));

  const getBudgetInputs = (): Input[] => budgetInput(getErrorMessages());

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
