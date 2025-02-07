import { defineStore } from "pinia";
import { ref } from "vue";

export const useMessageStore = defineStore("message", () => {
  const errorCurrentMessage = ref("");
  const successCurrentMessage = ref("");
  const successMessage ={
    default:{
      login:"Nie znany błąd",
      logOut:"Nie znany błąd",
    },
    login:"Zalogowanie pomyślnie",
    logOut:"Wylogowano pomyślnie"
  }
  const errorMessage = {
    default: {
      response: "nie znany błąd",
      wrongLoginAndPass: "Nie znany komunikat",
    },
    login: {
      response: "Błąd logowania",
      wrongLoginAndPass: "Błędny login lub hasło.",
      
    },
    validationRules: {
      unknow: "Unknown error",
      required: "Field cannot be empty",
      minLength: "Field must be at least {0} characters long",
      maxLength: "Field cannot be longer than {0} characters",
      forbiddenChars: "Field contains forbidden character: {0}",
      equalLength: "Field must be exactly {0} characters long",
      pattern: "Field does not match the required pattern",
      email: "Invalid email format",
      number: "Field must be a number",
      startsWith: "Field must start with {0}",
      endsWith: "Field must end with {0}",
      isEqual: "Fields must be equal",
      isInRange: "Field must be between {0} and {1}",
      doCheckbox: "You must check this box.",
    },
  };
  const responseError = (type: keyof typeof errorMessage) =>
    "response" in errorMessage[type]
      ? errorMessage[type].response
      : errorMessage.default.response;

  const loginError = () =>
    errorMessage.login.wrongLoginAndPass ||
    errorMessage.default.wrongLoginAndPass;
  const loginSuccess = () => successMessage.login || successMessage.default.login;
  const logOutSuccess = () => successMessage.logOut || successMessage.default.logOut;
  const getValidationRules = () => errorMessage.validationRules;

  const setErrorCurrentMessage = (error: string) =>
    (errorCurrentMessage.value = error);
  const setSuccessCurrentMessage = (success: string) =>
    (successCurrentMessage.value = success);
  return {
    responseError,
    loginError,
    loginSuccess,
    getValidationRules,
    setErrorCurrentMessage,
    errorCurrentMessage,
    setSuccessCurrentMessage,
    successCurrentMessage,
    logOutSuccess,
  };
});
