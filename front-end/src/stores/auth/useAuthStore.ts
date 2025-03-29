import { defineStore } from "pinia";
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { useNotificationStore } from "../ui/useNotificationStore";
import router from "@/router";
import { TOKEN } from "@/type";
import {usePermissionStore} from "@/stores"
import {
  loginFetch,
  registerFetch,
  fetchRefreshToken,
  fetchVerify,
  fetchLogOut,
  fetchPermission
} from "@/api/auth";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const {
      loginSuccess,
      setErrorCurrentMessage,
      setSuccessCurrentMessage,
      logOutSuccess,
      unexpectedError,
    } = useNotificationStore();
    const {hasPermission} =usePermissionStore()
    const token = ref<TOKEN | null>(null);
    const getPermission = useMutation({
      mutationFn: fetchPermission,
    });
      
    const checkPermission =async (name: string | undefined, type: "nav" | "path" = "nav") =>{
      const userPermission = await getPermission.mutateAsync() || [];
      return hasPermission(userPermission,name,type);
    }
    const validToken = async (): Promise<boolean> => {
      if (token.value) {
        try {
          const verify = await fetchVerify(
            getToken() || { access: "", refresh: "" }
          );
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
      if (!token.value) {
        setErrorCurrentMessage(unexpectedError());
        return false;
      }
      try {
        const tokenRefresh: TOKEN = await fetchRefreshToken(token.value);
        if (tokenRefresh) {
          saveToken(tokenRefresh);
          return true;
        }
      } catch (error: any) {
        setErrorCurrentMessage(error.message);
        return false;
      }
      return false;
    };

    const saveToken = (data: TOKEN) => {
      token.value = data;
    };
    const getToken = () => {
      return token.value;
    };
    const logout = () => {
      logOutMutation.mutateAsync();
    };
    const isLogin = async () => {
      if (!!token) {
        return true;
      }
      return false;
    };
    const logOutMutation = useMutation({
      mutationFn: fetchLogOut,
      onSuccess: () => {
        setSuccessCurrentMessage(logOutSuccess());
        token.value = null;
        router.push({ name: "landing" });
      },
      onError: (err) => {
        setErrorCurrentMessage(err.message);
      },
    });
    const loginMutation = useMutation({
      mutationFn: loginFetch,
      onSuccess: (data: TOKEN) => {
        setSuccessCurrentMessage(loginSuccess());
        saveToken(data);
        router.push({ name: "landing" });
      },
      onError: (err) => {
        setErrorCurrentMessage(err?.message || unexpectedError());
      },
    });

    const registerMutation = useMutation({
      mutationFn: registerFetch,
      onSuccess: (data) => {
        setSuccessCurrentMessage("Success");
        router.push("/logIn");
      },
      onError: (err) => {
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
      refreshToken,
      checkPermission
    };
  },
  {
    persist: {
      storage: localStorage,
      pick: ["token"],
    },
  }
);
