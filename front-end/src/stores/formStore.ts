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
  const extraError = {
    isEqual: "Hasła muszą być takie same",
    dateRange: "Data zakończenia nie może być wcześniejsza niż rozpoczęcia",
  };
  const getLoginInput = (): Input[] => loginInput(errorMessage());

  const getRegisterInput = (): Input[] =>
    registerInput(errorMessage({ isEqual: extraError.isEqual }));

  const getPlanInput = (): Input[] =>
    planInput(errorMessage({ dateRange: extraError.dateRange }));

  const getTripInput = (): Input[] =>
    tripInput(errorMessage({ dateRange: extraError.dateRange }));

  const getBudgetInput = (): Input[] => budgetInput(errorMessage());

  const formInputsMap: Record<FormType, () => Input[]> = {
    [FormType.LOGIN]: getLoginInput,
    [FormType.REGISTER]: getRegisterInput,
    [FormType.PLAN]: getPlanInput,
    [FormType.TRIP]: getTripInput,
    [FormType.BUDGET]: getBudgetInput,
  };
  const getFormInputs = (type: FormType): Input[] =>
    formInputsMap[type]?.() ?? [];

  const validateForm = (type: FormType, formValues: Record<string, string>) => {
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
  return { getFormInputs, validateForm, getMoreOptions };
});
