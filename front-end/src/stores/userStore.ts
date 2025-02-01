import { defineStore } from "pinia";
import { ref } from "vue";
import { useMessageStore } from "@/stores/messageStore";

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("jwt") || null);
  interface TOKEN {
    refresh: string;
    access: string;
  }
  const getToken = async (tokenRefresh: string) => {
    try {
      const response = await fetch(
        "https://api.plannder.com/user_auth/token/refresh/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            //"Bearer":token
          },
          body: JSON.stringify({ refresh: tokenRefresh }),
        }
      );
      if (!response.ok) {
        console.log("error");
        throw new Error("refresh error");
      }
      const data: TOKEN = await response.json();
      localStorage.setItem("jwt", JSON.stringify(data));
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };
  const login = async (credentials: Record<string, string>) => {
    const messageStore = useMessageStore();
    console.log(credentials);
    try {
      const response = await fetch(
        "https://api.plannder.com/user_auth/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            //"Bearer":token
          },
          body: JSON.stringify(credentials),
        }
      );
      if (!response.ok) {
        console.log(messageStore.responseError("login"));
        throw new Error(messageStore.responseError("login"));
      }

      const data: TOKEN = await response.json();
      localStorage.setItem("jwt", JSON.stringify(data));
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };
  const isLogin = () => {
    let token: TOKEN | null = !localStorage.getItem("jwt")
      ? null: localStorage.getItem("jwt");
      console.log(token);
    if (token) {
      return getToken(token.refresh);
    }
    return true;
  };
  const logout = () => {
    token.value = null;
    localStorage.removeItem("jwt");
  };

  const isAuthenticated = () => !!token.value;

  return { login, isLogin, logout, isAuthenticated };
});
