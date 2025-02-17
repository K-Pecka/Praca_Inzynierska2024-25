import {TOKEN} from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
export const fetchRefreshToken = async (token:TOKEN) =>{
    const response = await fetch(apiEndpoints.auth.refreshToken, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({refresh:token.refresh}),
    });
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData || "error");
    }
    return response.json();
  }