import { defineStore } from "pinia";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { useNotificationStore } from "../ui/useNotificationStore";
import router from "@/router";
import { TOKEN } from "@/type";
import {loginFetch,registerFetch,fetchRefreshToken,fetchVerify} from "@/api/auth"

export const useAuthStore = defineStore("auth", () => {
  const { loginSuccess, setErrorCurrentMessage, setSuccessCurrentMessage,logOutSuccess } = useNotificationStore();
  const token = ref<TOKEN | null>(null);
  const validToken = async (): Promise<boolean> => {
    if (token.value) {
      try {
        const verify = await fetchVerify(getToken() || {access:"",refresh:""});
        if (verify) {
          return true;
        } else {
          return false;
        }
      } catch (error) {
        return false;
      }
    }
    return false;
  };
  
  const refreshToken = async (): Promise<Boolean> => {
    if (token.value) {
      try {
        const tokenRefresh:TOKEN = await fetchRefreshToken(token.value);
        if(tokenRefresh){
          console.log(`${tokenRefresh}`);
          saveToken(tokenRefresh);
          return true
        }
  
      } catch (error) {
        setErrorCurrentMessage("Wystąpił błąd podczas odświeżania tokena");
        console.error("Error refreshing token:", error);
        return false;
      }
    } else {
      setErrorCurrentMessage("Brak tokena");
      return false;
    }
  
    return false;
  };
  
  const saveToken = (data: TOKEN) => {
    token.value = data;
  };
  const getToken = () =>{
    return token.value
  }
  const logout = () => {
    token.value = null;
    setSuccessCurrentMessage(logOutSuccess())
    router.push({name:'landing'});
  };
  const isLogin = async () => {
    if (!!token) {
      return true;
    }
    return false;
  };
  const loginMutation = useMutation({
    mutationFn: loginFetch,
    onSuccess: (data:TOKEN) => {
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
    token,
    loginMutation, 
    registerMutation, 
    saveToken,
    logout, 
    isLogin,
    validToken,
    getToken,
    refreshToken
  };
},{
  persist: {
    storage: localStorage,
    pick: ['token'],
  },
});
