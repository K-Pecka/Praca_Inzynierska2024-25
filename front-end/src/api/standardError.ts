import { useAuthStore,useUtilStore } from "@/stores" 
const unauthorized = async () =>{
    const {getToken,refreshToken} = useAuthStore();
    const token = getToken()?.access;
    if (token) {
        return refreshToken();
    }else{
        return false;
    }
}
const serverError = async () =>{
    const {useRouter} = useUtilStore();
    useRouter().push({name:"error_500"})
}
const noFoundError = async () =>{
    const {useRouter} = useUtilStore();
    useRouter().push({name:"error_404"})
}
export const statusType: { [key: number]: () => void } = {
    401:unauthorized,
    404:noFoundError,
    500:serverError
}
export const errorStatus = (status:number) =>{
    return statusType[status]?.() ?? null
}