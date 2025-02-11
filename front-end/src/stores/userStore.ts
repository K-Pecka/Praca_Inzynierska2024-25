import { defineStore } from "pinia";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { Register } from "@/type/interface";
import { useMessageStore } from "./messageStore";
import router from "@/router";

interface TOKEN {
  refresh: string;
  access: string;
}

export const useUserStore = defineStore("user", () => {
  const { loginError, loginSuccess, setErrorCurrentMessage, setSuccessCurrentMessage } = useMessageStore();
  const token = ref<TOKEN | null>(
    localStorage.getItem("jwt") ? JSON.parse(localStorage.getItem("jwt") as string) : null
  );

  const saveToken = (data: TOKEN) => {
    token.value = data;
    localStorage.setItem("jwt", JSON.stringify(data));
  };

  const logout = () => {
    token.value = null;
    localStorage.removeItem("jwt");
  };
  const isLogin = async () => {
    let token: TOKEN | null = !localStorage.getItem("jwt")
      ? null : JSON.parse(localStorage.getItem("jwt") as string) as TOKEN;
    if (token) {
      return true;
    }
    return false;
  };
  const isAuthenticated = () => !!token.value;

  const login = async (credentials: Record<string, string>) => {
    const response = await fetch("https://api.plannder.com/user_auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData || loginError());
    }
    return response.json();
  };

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      setSuccessCurrentMessage(loginSuccess());
      saveToken(data);
      router.push("/panel");
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message);
    },
  });

  const register = async (userData: Register) => {
    const response = await fetch("https://api.plannder.com/user/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    console.log(userData);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData || "unknow");
    }

    return response.json();
  };

  const registerMutation = useMutation({
    mutationFn: register,
    onSuccess: (data) => {
      setSuccessCurrentMessage("Success");
      console.log(data);
      //router.push("/logIn");
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
    isAuthenticated, 
    token,
    isLogin
  };
});
