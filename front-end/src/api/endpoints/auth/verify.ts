import apiClient from "@/api/apiClient";
import { TOKEN } from "@/types/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
import { errorStatus } from "@/api/standardError";
import { APP_MODE_DEV } from "@/config/envParams";

export const fetchVerify = async (token: TOKEN) => {
    if (APP_MODE_DEV) {
        return {};
    }

    try {
        const response = await apiClient.post(apiEndpoints.auth.verify, {
            token: token.access,
        });

        return response.data;
    } catch (error: any) {
        if (error.response?.status) {
            throw new Error(errorStatus(error.response.status) || "Wystąpił błąd");
        }
        throw new Error("Wystąpił błąd");
    }
};