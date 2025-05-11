import apiClient from "@/api/apiClient";
import { Register } from "@/types/interface";
import { apiEndpoints } from "@/api/apiEndpoints";

export const registerFetch = async (userData: Register) => {
    try {
        const response = await apiClient.post(apiEndpoints.auth.register, userData);
        return response.data;
    } catch (error: any) {
        const errorData = error.response?.data;
        throw new Error(errorData || "unknown");
    }
};