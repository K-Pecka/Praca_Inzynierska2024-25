import { defineStore } from "pinia";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { useMessageStore } from "./messageStore";
import router from "@/router";
import { TOKEN } from "@/type";
import {loginFetch,registerFetch,fetchRefreshToken} from "@/api/auth"

export const useUserStore = defineStore("user", () => {
  const { loginSuccess, setErrorCurrentMessage, setSuccessCurrentMessage,logOutSuccess } = useMessageStore();
  const token = ref<TOKEN | null>(
    localStorage.getItem("jwt") ? JSON.parse(localStorage.getItem("jwt") as string) : null
  );
  const getToken = async () => {
    if (token.value) {
      const tokenRefresh = await fetchRefreshToken(token.value);
      saveToken(tokenRefresh);
      token.value = tokenRefresh;
      return token.value?.access || "";
    }
    else{
      router.push({name:'landing'});
    }
    return "";
  }
  const saveToken = (data: TOKEN) => {
    token.value = data;
    localStorage.setItem("jwt", JSON.stringify(data));
  };

  const logout = () => {
    token.value = null;
    localStorage.removeItem("jwt");
    setSuccessCurrentMessage(logOutSuccess())
    router.push({name:'landing'});
  };
  const isLogin = async () => {
    let token: TOKEN | null = !localStorage.getItem("jwt")
      ? null : JSON.parse(localStorage.getItem("jwt") as string) as TOKEN;
    if (token) {
      return true;
    }
    return false;
  };
  const loginMutation = useMutation({
    mutationFn: loginFetch,
    onSuccess: (data) => {
      setSuccessCurrentMessage(loginSuccess());
      saveToken(data);
      router.push("/panel");
    },
    onError: (err) => {
      setErrorCurrentMessage("An unexpected error occurred.");
    },
  });

  const registerMutation = useMutation({
    mutationFn: registerFetch,
    onSuccess: (data) => {
      setSuccessCurrentMessage("Success");
      router.push("/logIn");
    },
    onError: (err) => {
      console.log(err);
      setErrorCurrentMessage("Error");
    },
  });

  return { 
    loginMutation, 
    registerMutation, 
    logout, 
    isLogin,
    getToken
  };
});
