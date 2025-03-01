import {TOKEN} from "@/type/interface";
import { apiEndpoints } from "@/api/apiEndpoints";
import { errorStatus } from "@/api/standardError";
export const fetchVerify = async (token:TOKEN,tryAgain:Boolean =true) =>{
    try{
      const response = await fetch(apiEndpoints.auth.verify, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({token:token.access}),
    });
    if (!response.ok && tryAgain) {
      console.log("błąd 401");
      console.log(!errorStatus(response.status))
      console.log(token);
      if(!errorStatus(response.status))
      {
        console.log(token);
        fetchVerify(token,false);
      }
    }
    return response.json();
    }
    catch(error){
      console.log("error");
    }
  }