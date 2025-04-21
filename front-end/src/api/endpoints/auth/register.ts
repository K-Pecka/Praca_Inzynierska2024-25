import {Register} from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";

export const registerFetch = async (userData: Register) => {
    const response = await fetch(apiEndpoints.auth.register, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData || "unknow");
    }

    return response.json();
  };