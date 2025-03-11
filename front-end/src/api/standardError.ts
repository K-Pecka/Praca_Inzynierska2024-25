import { useAuthStore } from "@/stores" 
import { useUtilStore } from "@/stores";
const Unauthorized = async () =>{
    const {getToken,refreshToken} = useAuthStore();
    const token = getToken()?.access;
    if (token) {
        return refreshToken();
    }else{
        return false;
    }
}
const ServerError = async () =>{
    const {useRouter} = useUtilStore();
    useRouter().push({name:"error_500"})
}
export const statusType: { [key: number]: () => void } = {
    401:Unauthorized,
    500:ServerError
}
export const errorStatus = (status:number) =>{
    return statusType[status]?.() ?? null
}