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

  const responseError = () => messages.error.login.response || messages.error.default;
  const loginError = () => messages.error.login.wrongLoginAndPass || messages.error.default;
  const loginSuccess = () => messages.success.login || messages.success.default;
  const logOutSuccess = () => messages.success.logOut || messages.success.default;

  return {
    errorCurrentMessage,
    successCurrentMessage,

    loginSuccessMessage,
    logOutSuccessMessage,

    setErrorCurrentMessage,
    setSuccessCurrentMessage,
    responseError,
    loginError,
    loginSuccess,
    logOutSuccess,
  };
});
