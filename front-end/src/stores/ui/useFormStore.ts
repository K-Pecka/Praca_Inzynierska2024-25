import { defineStore } from "pinia";
import { ref } from "vue";
import { Input } from "@/types/interface";
import { FormType } from "@/types/enum";
import {
  loginInput,
  registerInput,
  planInput,
  tripInput,
  budgetInput,
  profilePersonalInput,
  profilePasswordInput,
  getMoreOptions,
} from "@/data/index";
import { useNotificationStore } from "@/stores";

export const useFormStore = defineStore("form", () => {
  const { getErrorMessages } = useNotificationStore();

  const currentFormType = ref<FormType>(FormType.LOGIN);
  const isSending = ref(false);
  const backendErrors = ref<Record<string, Record<string, string>>>({});
  const formValues = ref<Record<string, string>>({});

  const extraValidationMessages = {
    isEqual: "Hasła muszą być takie same",
    dateRange: "Data zakończenia nie może być wcześniejsza niż rozpoczęcia",
  };

  const getLoginInputs = (): Input[] => loginInput(getErrorMessages());
  const getRegisterInputs = (): Input[] =>
    registerInput(
      getErrorMessages({ isEqual: extraValidationMessages.isEqual })
    );
  const getPlanInputs = (): Input[] =>
    planInput(
      getErrorMessages({ dateRange: extraValidationMessages.dateRange })
    );
  const getTripInputs = (): Input[] =>
    tripInput(
      getErrorMessages({ dateRange: extraValidationMessages.dateRange })
    );
  const getBudgetInputs = (): Input[] => budgetInput(getErrorMessages());

  const getProfilePersonalInputs = (): Input[] =>
      profilePersonalInput(getErrorMessages());

  const getProfilePasswordInputs = (): Input[] =>
      profilePasswordInput(getErrorMessages({ isEqual: extraValidationMessages.isEqual }));

  const formInputGenerators: Record<FormType, () => Input[]> = {
    [FormType.LOGIN]: getLoginInputs,
    [FormType.REGISTER]: getRegisterInputs,
    [FormType.PLAN]: getPlanInputs,
    [FormType.TRIP]: getTripInputs,
    [FormType.BUDGET]: getBudgetInputs,
    [FormType.PROFILE_PERSONAL]: getProfilePersonalInputs,
    [FormType.PROFILE_PASSWORD]: getProfilePasswordInputs
  };

  const getFormInputs = (type: FormType): Input[] =>
    formInputGenerators[type]?.() ?? [];

  const initForm = (type: FormType) => {
    currentFormType.value = type;
    formValues.value = createFormValues(type);
    return {inputs:getFormInputs(type),values: formValues.value};
  };

  const createFormValues = (type: FormType): Record<string, string> => {
    const inputs = getFormInputs(type);
    return Object.fromEntries(inputs.map((input) => [input.name, ""]));
  };

  const isFormValid = (
    type: FormType,
    values: Record<string, string>
  ): boolean =>
    getFormInputs(type).every((input) => {
      const value = values[input.name];
      let errors: string[] = [];

      if (input.validation && "validate" in input.validation) {
        errors = input.validation.validate(value);
      }

      input.error = [...errors];
      return errors.length === 0;
    });

  const sendForm = async ({
    send,
    onSuccess,
    onError,
    data,
  }: {
    send: (formData: Record<string, any>) => Promise<void>;
    onSuccess?: () => void;
    onError?: (error: any) => void;
    data: Record<string, string>;
  }) => {
    if (isFormValid(currentFormType.value, data) && !isSending.value) {
      isSending.value = true;
      try {
        await send(data);
        formValues.value = createFormValues(currentFormType.value);
        onSuccess?.();
      } catch (error) {
        onError?.(error);
      } finally {
        isSending.value = false;
      }
    } else {
      const { setErrorCurrentMessage } = useNotificationStore();
      setErrorCurrentMessage("Uzupełnij wszystkie wymagane pola poprawnie.");
    }
  };

  const setBackendErrors = (error: Record<string, any>) => {
    backendErrors.value[currentFormType.value] = error;
  };

  const getBackendErrors = () => backendErrors.value;

  return {
    currentFormType,
    formValues,
    isSending,
    initForm,
    getFormInputs,
    isFormValid,
    sendForm,
    setBackendErrors,
    getBackendErrors,
    getMoreOptions,
    getProfilePersonalInputs,
    getProfilePasswordInputs
  };
});
