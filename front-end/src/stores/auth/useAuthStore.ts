import { defineStore } from "pinia";
import { ref } from "vue";
import { useMutation, useQuery } from "@tanstack/vue-query";
import { useNotificationStore } from "@/stores/ui/useNotificationStore";
import router from "@/router";
import { TOKEN, User } from "@/types";
import { usePermissionStore } from "@/stores";
import {
  loginFetch,
  registerFetch,
  fetchRefreshToken,
  fetchVerify,
  fetchLogOut,
  fetchPermission,
  updateUser,
} from "@/api/endpoints/auth";
import {getMutationUpdateUser} from "@/api/services/userQuery"
import { nextTick } from "vue";
import { queryClient } from "@/main";
import { useRoleStore } from "./useRoleStore";
export const useAuthStore = defineStore(
  "auth",
  () => {
    const notification = useNotificationStore()
    const {
      loginSuccess,
      setErrorCurrentMessage,
      setSuccessCurrentMessage,
      logOutSuccess,
      unexpectedError,
    } = useNotificationStore();
    const { hasPermission } = usePermissionStore();
    const token = ref<TOKEN | null>(null);
    const user = ref<User | null>(null);
    const getUser = () => user.value;
    const getPermission = useQuery({
      queryKey: ["permission",getUser()?.profiles?.[0]?.id],
      queryFn: fetchPermission,
      enabled: getUser()?.profiles?.[0]?.id !== undefined,
    });

    const checkPermission = async (
      name: string | undefined,
      type: "nav" | "path" = "nav"
    ) => {
      return true//hasPermission(userPermission, name, type);
    };
    const validToken = async (): Promise<boolean> => {
      const currentToken = getToken();
      if (!currentToken?.access || !currentToken?.refresh) return false;

      try {
        await fetchVerify(currentToken);
        return true;
      } catch {
        try {
         // const refreshed = await refreshToken();
          //if (!refreshed) return false;
          await fetchVerify(getToken()!);
          return true;
        } catch {
          return false;
        }
      }
    };


    const saveToken = (data: TOKEN) => {
      token.value = data;
    };
    const saveUser = (data: User): void => {
      user.value = data;
    };
    const isOwner = (id: number) => getUser()?.profiles?.some(profile => profile.id === id) ?? false;

    const getToken = () => {
      return token.value;
    };
    function setActiveProfile(profileId: number) {
      if (!user.value || !user.value.profiles) return;
      user.value.profiles = user.value.profiles.map(p => ({
        ...p,
        is_default: p.id === profileId,
      }));
    }
    const logout = async () => {
      try {
        await logOutMutation.mutateAsync();
      } catch (err: any) {
        setErrorCurrentMessage(
          err?.message || "Nie można wylogować (token wygasł?)"
        );
      } finally {
        token.value = null;
        user.value = null;
        queryClient.clear();
        router.push({ name: "landing" });
      }
    };
    const isLogin = async () => {
      try {
        if (!!(await validToken())) {
          return true;
        }
      } catch (error) {
        return false;
      }
    };
    const logOutMutation = useMutation({
      mutationFn: fetchLogOut,
      onSuccess: () => {
        setSuccessCurrentMessage(logOutSuccess());
        token.value = null;
        user.value = null;
        useRoleStore().setRole("unknown");
        router.push({ name: "landing" });
      },
      onError: (err) => {
        setErrorCurrentMessage(err.message);
      },
    });
    const loginMutation = useMutation({
      mutationFn: loginFetch,
      onSuccess: async (data) => {
        const { access, refresh } = data;

        saveToken({ access, refresh });
        saveUser(data);
        setSuccessCurrentMessage(loginSuccess());

        await nextTick();

        await router.push({ name: "landing" });
      },
      onError: (err: any) => {
        setErrorCurrentMessage(err?.message || unexpectedError());
      },
    });

    const registerMutation = useMutation({
      mutationFn: registerFetch,
      onSuccess: (data) => {
        setSuccessCurrentMessage("Rejestracja zakończona sukcesem");
        router.push({ name: "login" });
      },
      onError: (err) => {
        setErrorCurrentMessage("Error");
      },
    });
    const userUpdate = getMutationUpdateUser({
        saveToken,
        notification,
        queryClient,
        successMessage: "Zaktualizowano dane",
        errorMessage: "Wystąpił problem przy zmianie danych",
    })
    const updateProfileMutation = useMutation({
      mutationFn: async (dto: {
        first_name?: string;
        last_name?: string;
      }) => {
          return updateUser(dto);
      },
      onSuccess: (data) => {
        if (data && user?.value) {
          user.value.first_name = data.first_name ?? user.value.first_name;
          user.value.last_name = data.last_name ?? user.value.last_name;
          setSuccessCurrentMessage("Zaktualizowano dane profilu");
        }
      },
      onError: (err: any) =>
        setErrorCurrentMessage(err?.message || unexpectedError()),
    });

    const updatePasswordMutation = useMutation({
      mutationFn: async (dto: {
          password: string;
          password_confirm: string
      }) => {
          if (!dto.password || !dto.password_confirm) {
              throw new Error("Hasło nie może być puste");
          }
          return updateUser(dto);
      },
      onSuccess: () => {
          setSuccessCurrentMessage("Hasło zostało zmienione");
      },
      onError: (err) => {
          setErrorCurrentMessage(err?.message || "Błąd przy zmianie hasła");
      },
    });

    const getUserInitials = () => {
      if (!user.value) return " ";
      const firstInitial = user.value.first_name
        ? user.value.first_name[0]
        : "";
      const lastInitial = user.value.last_name ? user.value.last_name[0] : "";
      return (firstInitial + lastInitial).toUpperCase() || " ";
    };

    return {
      setActiveProfile,
      userData: {
        getUser,
        isOwner,
      },
      userUpdate,
      token,
      user,
      loginMutation,
      registerMutation,
      saveToken,
      logout,
      isLogin,
      validToken,
      getToken,
      checkPermission,
      updateProfileMutation,
      updatePasswordMutation,
      getUserInitials,
      getUser,
    };
  },
  {
    persist: {
      storage: localStorage,
      pick: ["token", "user"],
    },
  }
);
