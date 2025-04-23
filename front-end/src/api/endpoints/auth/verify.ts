import {TOKEN} from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
import { errorStatus } from "@/api/standardError";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchVerify = async (token:TOKEN) =>{
  if (APP_MODE_DEV) {
    
    return {};
  }  
  const response = await fetch(apiEndpoints.auth.verify, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({token:token.access}),
    });
    if (!response.ok) {
      throw new Error(errorStatus(response.status) || "Wystąpił błąd");
    }
    return response.json();
  }