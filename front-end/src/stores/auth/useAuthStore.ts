import { defineStore } from "pinia";
import { ref, nextTick } from "vue";
import { useMutation, useQuery } from "@tanstack/vue-query";
import router from "@/router";
import { TOKEN, User } from "@/types";
import { useNotificationStore } from "@/stores/ui/useNotificationStore";
import { useFormStore, usePermissionStore } from "@/stores";
import {
  loginFetch,
  registerFetch,
  fetchVerify,
  fetchLogOut,
  fetchPermission,
  fetchPaymentUrl,
  updateUser
} from "@/api/endpoints/auth";
import { getMutationUpdateUser } from "@/api/services/userQuery";
import { queryClient } from "@/main";
import { useRoleStore } from "./useRoleStore";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const notificationStore = useNotificationStore();
    const permissionStore = usePermissionStore();
    const roleStore = useRoleStore();
    const formStore = useFormStore();

    const token = ref<TOKEN | null>(null);
    const user = ref<User | null>(null);

    const getUser = () => user.value;

    const saveToken = (data: TOKEN) => {
      token.value = data;
    };

    const saveUser = (data: User) => {
      user.value = data;
    };

    const getToken = () => token.value;

    const isOwner = (profileId: number) =>
      getUser()?.profiles?.some((profile) => profile.id === profileId) ?? false;

    const setActiveProfile = (profileId: number) => {
      if (!user.value?.profiles) return;
      user.value.profiles = user.value.profiles.map((p) => ({
        ...p,
        is_default: p.id === profileId,
      }));
    };

    const validToken = async (): Promise<boolean> => {
      const currentToken = getToken();
      if (!currentToken?.access || !currentToken?.refresh) return false;

      try {
        await fetchVerify(currentToken);
        return true;
      } catch {
        return false;
      }
    };

    const logout = async () => {
      try {
        await logOutMutation.mutateAsync();
      } catch (err: any) {
        notificationStore.setErrorCurrentMessage(
          err?.message || "Nie można wylogować (token wygasł?)"
        );
      } finally {
        token.value = null;
        user.value = null;
        queryClient.clear();
        router.push({ name: "landing" });
      }
    };

    const isLoggedIn = async (): Promise<boolean> => {
      try {
        return !!(await validToken());
      } catch {
        return false;
      }
    };

    const checkPermission = async (
      name: string | undefined,
      type: "nav" | "path" = "nav"
    ) => {
      return true;
    };

    const getPermissionQuery = useQuery({
      queryKey: ["permission", getUser()?.profiles?.[0]?.id],
      queryFn: fetchPermission,
      enabled: !!getUser()?.profiles?.[0]?.id,
    });

    const logOutMutation = useMutation({
      mutationFn: fetchLogOut,
      onSuccess: () => {
        notificationStore.setSuccessCurrentMessage("Wylogowano pomyślnie");
        token.value = null;
        user.value = null;
        roleStore.setRole("unknown");
        router.push({ name: "landing" });
      },
      onError: (err: any) => {
        notificationStore.setErrorCurrentMessage(err.message);
      },
    });

    const loginMutation = useMutation({
      mutationFn: loginFetch,
      onSuccess: async (data) => {
        saveToken({ access: data.access, refresh: data.refresh });
        saveUser(data);
        notificationStore.setSuccessCurrentMessage("Zalogowano pomyślnie");
        await nextTick();
        router.push({ name: "landing" });
      },
      onError: (err: any) => {
        notificationStore.setErrorCurrentMessage(
          err?.detail || "Nieoczekiwany błąd podczas logowania"
        );
      },
    });

    const registerMutation = useMutation({
      mutationFn: registerFetch,
      onSuccess: () => {
        notificationStore.setSuccessCurrentMessage(
          "Rejestracja zakończona sukcesem"
        );
        router.push({ name: "logIn" });
      },
      onError: (err: any) => {
        notificationStore.setErrorCurrentMessage(
          err?.detail || "Nieoczekiwany błąd podczas rejestracji"
        );
      },
    });

    const userUpdateMutation = getMutationUpdateUser({
      saveToken,
      notification: notificationStore,
      queryClient,
      successMessage: "Zaktualizowano dane",
      errorMessage: "Wystąpił problem z zmianą danych",
    });

    const updateProfileMutation = useMutation({
      mutationFn: async (dto: {
        first_name?: string;
        last_name?: string;
      }) => {
          return updateUser(dto);
      },
      onSuccess: (data) => {
        if (data && user.value) {
          user.value.first_name = data.first_name ?? user.value.first_name;
          user.value.last_name = data.last_name ?? user.value.last_name;
          notificationStore.setSuccessCurrentMessage(
            "Zaktualizowano dane profilu"
          );
        }
      },
      onError: (err: any) =>
        notificationStore.setErrorCurrentMessage(
          err?.message || "Nieoczekiwany błąd podczas aktualizacji profilu"
        ),
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
          notificationStore.setSuccessCurrentMessage("Hasło zostało zmienione");
      },
      onError: (err) => {
          notificationStore.setErrorCurrentMessage(err?.message || "Błąd przy zmianie hasła");
      },
    });

    const getUserInitials = (): string => {
      if (!user.value) return " ";
      const firstInitial = user.value.first_name?.[0] ?? "";
      const lastInitial = user.value.last_name?.[0] ?? "";
      return (firstInitial + lastInitial).toUpperCase() || " ";
    };
    const getActiveProfile = () => {
      return user.value?.profiles?.find((profile) => profile.is_default) || null;
    }
    const isGuide = () => getUser()?.profiles?.find((profile) => profile.type == 2)?.is_default ?? false;
    const startCheckout  = useMutation({
      mutationFn: fetchPaymentUrl,
      onSuccess: (data) => {
        window.location.href = data?.checkout_url;
      },
      onError: (err: any) =>{
        notificationStore.setErrorCurrentMessage(
          err?.detail || "Błąd"
        )
        if(!getUser()){
          router.push({name:"logIn"})
        }
      }
    });

    return {
      startCheckout,
      userData: {
        getUser,
        isOwner,
        getActiveProfile
      },
      isGuide,
      token,
      user,
      saveToken,
      saveUser,
      getToken,
      setActiveProfile,
      validToken,
      logout,
      isLoggedIn,
      checkPermission,
      getPermissionQuery,
      loginMutation,
      registerMutation,
      userUpdateMutation,
      updateProfileMutation,
      updatePasswordMutation,
      getUserInitials,
    };
  },
  {
    persist: {
      key: 'auth',
      storage: localStorage
    },
  }
);
