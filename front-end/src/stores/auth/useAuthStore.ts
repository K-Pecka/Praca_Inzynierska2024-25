import {defineStore} from "pinia";
import {ref} from "vue";
import {useMutation} from "@tanstack/vue-query";
import {useNotificationStore} from "../ui/useNotificationStore";
import router from "@/router";
import {TOKEN} from "@/type";
import {usePermissionStore} from "@/stores";
import {
    loginFetch,
    registerFetch,
    fetchRefreshToken,
    fetchVerify,
    fetchLogOut,
    fetchPermission,
} from "@/api/endpoints/auth";
import { useMockupStore } from '@/mockup/useMockupStore';

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
        const user = ref<{ first_name: string; last_name: string } | null>(null);
        const getPermission = useMutation({
            mutationFn: fetchPermission,
        });

        const checkPermission = async (
            name: string | undefined,
            type: "nav" | "path" = "nav"
        ) => {
            const userPermission = (await getPermission.mutateAsync()) || [];
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
                console.warn("refreshToken", tokenRefresh);
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
        const saveUser = (data: { first_name: string; last_name: string }) => {
            user.value = data;
        };

        const getToken = () => {
            return token.value;
        };
        const logout = () => {
            logOutMutation.mutateAsync();
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
                router.push({name: "landing"});
            },
            onError: (err) => {
                setErrorCurrentMessage(err.message);
            },
        });
        const loginMutation = useMutation({
            mutationFn: loginFetch,
            onSuccess: (data) => {
                const {access, refresh, last_name, first_name} = data;
                setSuccessCurrentMessage(loginSuccess());
                saveToken({access, refresh});
                saveUser({last_name, first_name});
                router.push({name: "landing"});
            },
            onError: (err) => {
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

        const { updateProfileMockUp } = useMockupStore();

        const updateProfileMutation = useMutation({
            mutationFn: async (dto: {
                first_name?: string; last_name?: string;
                current_password?: string; new_password?: string;
            }) => {
                const res = updateProfileMockUp(dto);
                if ((res as any).error) throw new Error((res as any).message);
                return res;
            },
            onSuccess: ({first_name, last_name}) => {
                if (first_name && last_name) {
                    saveUser({first_name, last_name});
                    setSuccessCurrentMessage('Zaktualizowano dane profilu');
                }
            },
            onError: (err: any) =>
                setErrorCurrentMessage(err?.message || unexpectedError()),
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
            checkPermission,
            updateProfileMutation,
        };
    },
    {
        persist: {
            storage: localStorage,
            pick: ["token", "user"],
        },
    }
);
