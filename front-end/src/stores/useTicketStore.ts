import { defineStore } from "pinia";
import { useUtilStore } from "./utils/useUtilStore";
export const useTicketStore = defineStore("ticket", () => {
    const {getTripId} = useUtilStore();
   const createTicket = (file:File,data:Record<string, string>) =>{
    console.log(file,data,getTripId());
    console.log(data);
    console.log(getTripId());
   }
    return {createTicket}
});