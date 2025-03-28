import {TOKEN} from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
import { errorStatus } from "@/api/standardError";
import { APP_MODE_DEV } from "@/config/envParams";
export const fetchVerify = async (token:TOKEN,tryAgain:Boolean =true) =>{
  if (APP_MODE_DEV) {
    return {};
  }  
  const response = await fetch(apiEndpoints.auth.verify, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({token:token.access}),
    });
    console.count("weryfikacja");
    if (!response.ok && tryAgain) {
      if(!errorStatus(response.status))
      {
        fetchVerify(token,false);
      }
    }
    return response.json();
  }