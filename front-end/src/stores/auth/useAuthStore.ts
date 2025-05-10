import {defineStore} from "pinia";
import {ref} from "vue";
import {useMutation} from "@tanstack/vue-query";
import {useNotificationStore} from "@/stores/ui/useNotificationStore";
import router from "@/router";
import {TOKEN, User} from "@/types";
import {usePermissionStore} from "@/stores";
import {
    loginFetch,
    registerFetch,
    fetchRefreshToken,
    fetchVerify,
    fetchLogOut,
    fetchPermission,
} from "@/api/endpoints/auth";
import {nextTick} from "vue";

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
        const {hasPermission} = usePermissionStore();
        const token = ref<TOKEN | null>(null);
        const user = ref<User | null>(null);
        const getPermission = useMutation({
            mutationFn: fetchPermission,
        });

        const checkPermission = async (
            name: string | undefined,
            type: "nav" | "path" = "nav"
        ) => {
            const userPermission = (await getPermission.mutateAsync()) as number[] || [];
            return hasPermission(userPermission, name, type);
        };
        const validToken = async (): Promise<boolean> => {
            if (token.value) {
                try {
                    const verify = await fetchVerify(
                        getToken() || {access: "", refresh: ""}
                    );
                    return true;
                } catch (error) {
                    await refreshToken();
                    try {
                        const verify = await fetchVerify(
                            getToken() || {access: "", refresh: ""}
                        );
                        return true;
                    } catch (error) {
                        return false;
                    }
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
                token.value = null;
                return false;
            }
            return false;
        };

        const saveToken = (data: TOKEN) => {
            token.value = data;
        };
        const saveUser = (data: User): void => {
            user.value = data;
        };
        const isOwner = (id: number) => id === (getUser()?.profiles?.[0]?.id ?? -1);
        const getUser = () => (user.value)
        const getToken = () => {
            return token.value;
        };
        const logout = async () => {
            try {
                await logOutMutation.mutateAsync();
            } catch (err: any) {
                setErrorCurrentMessage(err?.message || "Nie można wylogować (token wygasł?)");
            } finally {
                token.value = null;
                user.value = null;
                router.push({name: "landing"});
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
                router.push({name: "landing"});
            },
            onError: (err) => {
                setErrorCurrentMessage(err.message);
            },
        });
        const loginMutation = useMutation({
            mutationFn: loginFetch,
            onSuccess: async (data) => {
                const {access, refresh} = data;

                saveToken({access, refresh});
                saveUser(data);
                setSuccessCurrentMessage(loginSuccess());

                await nextTick();

                await router.push({name: "landing"});
            },
            onError: (err: any) => {
                setErrorCurrentMessage(err?.message || unexpectedError());
            },
        });

        const registerMutation = useMutation({
            mutationFn: registerFetch,
            onSuccess: (data) => {
                setSuccessCurrentMessage("Rejestracja zakończona sukcesem");
                router.push({name: "login"});
            },
            onError: (err) => {
                setErrorCurrentMessage("Error");
            },
        });

        const updateProfileMutation = useMutation({
            mutationFn: async (dto: {
                first_name?: string; last_name?: string;
                current_password?: string; new_password?: string;
            }) => {

                return {
                    first_name: dto.first_name || user.value?.first_name || '',
                    last_name: dto.last_name || user.value?.last_name || '',
                    userId: 0
                };
            },
            onSuccess: (data) => {
                if (data && user?.value) {
                    user.value.first_name = data.first_name;
                    user.value.last_name = data.last_name;
                    setSuccessCurrentMessage('Zaktualizowano dane profilu');
                }
            },
            onError: (err: any) =>
                setErrorCurrentMessage(err?.message || unexpectedError()),
        });
        const getUserInitials = () => {
            if (!user.value) return " ";
            const firstInitial = user.value.first_name ? user.value.first_name[0] : "";
            const lastInitial = user.value.last_name ? user.value.last_name[0] : "";
            return (firstInitial + lastInitial).toUpperCase() || " ";
        };

        return {
            userData: {
                getUser,
                isOwner
            },
            token,
            user,
            loginMutation,
            registerMutation,
            saveToken,
            logout,
            isLogin,
            validToken,
            getToken,
            refreshToken,
            checkPermission,
            updateProfileMutation,
            getUserInitials,
            getUser
        };
    },
    {
        persist: {
            storage: localStorage,
            pick: ["token", "user"],
        },
    }
);
