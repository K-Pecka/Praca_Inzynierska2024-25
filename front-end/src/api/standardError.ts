import { useUserStore } from "@/stores" 
const Unauthorized = async () =>{
    const {getToken,refreshToken} = useUserStore();
    const token = getToken()?.access;
    if (token) {
        console.log("refresh token");
        return refreshToken();
    }else{
        return false;
    }
}
export const statusType: { [key: number]: () => void } = {
    401:Unauthorized,
}
export const errorStatus = (status:number) =>{
    return statusType[status]?.() ?? null
}