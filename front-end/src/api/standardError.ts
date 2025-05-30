import { useAuthStore,useUtilsStore } from "@/stores"
const serverError = async () =>{
    const {useRouter} = useUtilsStore();
    //useRouter().push({name:"error_500"})
}
const noFoundError = async () =>{
    const {useRouter} = useUtilsStore();
    //useRouter().push({ name: "error_404", query: { message: "Podane żądanie nie istnieje.", code: "Błąd w żądaniu" } });
}
export const statusType: { [key: number]: () => void } = {
    404:noFoundError,
    403:noFoundError,
    500:serverError
}
export const errorStatus = (status:number) =>{
    return statusType[status]?.() ?? null
}