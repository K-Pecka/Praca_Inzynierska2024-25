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
    //useRouter().push({name:"error_500"})
}
const noFoundError = async () =>{
    const {useRouter} = useUtilStore();
    //useRouter().push({ name: "error_404", query: { message: "Podane żądanie nie istnieje.", code: "Błąd w żądaniu" } });
}
export const statusType: { [key: number]: () => void } = {
    401:unauthorized,
    404:noFoundError,
    403:noFoundError,
    500:serverError
}
export const errorStatus = (status:number) =>{
    return statusType[status]?.() ?? null
}