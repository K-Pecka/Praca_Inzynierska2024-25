import { defineStore } from "pinia";
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
import { computed, ref } from "vue";
import { useAuthStore,useNotificationStore } from "@/stores";

export const useFormStore = defineStore("form", () => {
  const { getErrorMessages } = useNotificationStore();
  const { loginMutation } = useAuthStore();
  const formType = ref<FormType>(FormType.LOGIN);
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
  const initForm = (type: FormType) => {
    formType.value = type;
    return getFormInputs(type);
  }
  const createformValues = () => {
    const inputs = getFormInputs(formType.value);
    return Object.fromEntries(inputs.map((input: { name: string }) => [input.name, ""]));
  };
  const isFormValid  = (type: FormType, formValues: Record<string, string>) => {
    return getFormInputs(type).every((input) => {
      const value = formValues[input.name];
      let errors: string[] = [];

      if (input.validation && "validate" in input.validation) {
        errors = input.validation.validate(value);
      }

      input.error = [...errors];
      return errors.length === 0;
    });
  };
  const isSend = ref(false);
  const sendForm =async (formValue: any, config: any)=>{
    console.log(config?.send,isFormValid(FormType.LOGIN, formValue),!isSend.value)
    if (config?.send && isFormValid(FormType.LOGIN, formValue) && !isSend.value) {
      isSend.value = true;
      try {
        await loginMutation.mutateAsync(formValue);
        formType.value = FormType.REGISTER;
      } catch (error) {
       console.log("Brak danych")
      }
      isSend.value = false
    }
  }
  const formValues = ref(createformValues())
  return { sendForm,initForm,formValues,getFormInputs, isFormValid, getMoreOptions };
});
