import { defineStore } from "pinia";
import { useUtilsStore } from "./utils/useUtilsStore";
export const useTicketStore = defineStore("ticket", () => {
    const {getTripId} = useUtilsStore();
   const createTicket = (file:File,data:Record<string, string>) =>{
   }
    return {createTicket}
});