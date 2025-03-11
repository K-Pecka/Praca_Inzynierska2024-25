import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useNotificationStore = defineStore("notification", () => {
  const errorCurrentMessage = ref("");
  const successCurrentMessage = ref("");

  const messages = {
    success: {
      login: "Zalogowano pomyślnie",
      logOut: "Wylogowano pomyślnie",
      default: "Operacja zakończona sukcesem",
    },
    error: {
      default: "Nieznany błąd",
      token: "Wystąpił problem związany z kontem, zostałeś wylogowany",
      login: {
        response: "Błąd logowania",
        wrongLoginAndPass: "Błędny login lub hasło",
      },
    },
  };

  const loginSuccessMessage = computed(() => messages.success.login);
  const logOutSuccessMessage = computed(() => messages.success.logOut);

  const setErrorCurrentMessage = (error: string) => {
    errorCurrentMessage.value = error;
  };

  const setSuccessCurrentMessage = (success: string) => {
    successCurrentMessage.value = success;
  };
  const getErrorMessages = (customErrors: Record<string, string> = {}) => ({
    unknown: "Nieznany błąd",
    required: "Pole nie może być puste",
    minLength: "Minimalna wymagana długość to {0} znaków",
    maxLength: "Pole nie może być dłuższe niż {0} znaków",
    forbiddenChars: "Pole zawiera niedozwolony znak: {0}",
    exactLength: "Pole musi mieć dokładnie {0} znaków",
    pattern: "Pole nie pasuje do wymaganego wzorca",
    email: "Nieprawidłowy format emaila",
    number: "Pole musi być liczbą",
    startsWith: "Pole musi zaczynać się od {0}",
    endsWith: "Pole musi kończyć się na {0}",
    mustMatch: "Pola muszą być równe",
    range: "Pole musi mieścić się w zakresie od {0} do {1}",
    minValue: "Wartość musi być większa niż {0}",
    ...customErrors,
  });
  const responseError = () => messages.error.login.response || messages.error.default;
  const loginError = () => messages.error.login.wrongLoginAndPass || messages.error.default;
  const loginSuccess = () => messages.success.login || messages.success.default;
  const logOutSuccess = () => messages.success.logOut || messages.success.default;
  const unexpectedError = () => messages.error.default;
  const tokenError = () => messages.error.token;
  return {
    errorCurrentMessage,
    successCurrentMessage,

    loginSuccessMessage,
    logOutSuccessMessage,
    unexpectedError,
    tokenError,
    getErrorMessages,
    setErrorCurrentMessage,
    setSuccessCurrentMessage,
    responseError,
    loginError,
    loginSuccess,
    logOutSuccess,
  };
});
