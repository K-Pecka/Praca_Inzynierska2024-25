import { defineStore } from "pinia";
import { ref } from "vue";
import { useUtilStore } from "@/stores/utils/useUtilStore";
interface Ticket {
    id: string;
    type: string;
    name: string;
    date: string;
    hour: string;
    assignedTo?: string;
    file: File;
}

interface TicketType {
    value: string;
    label: string;
    icon: string;
}

export const useTicketStore = defineStore("ticket", () => {
    const tickets = ref<Ticket[]>([]);

    const ticketTypes = ref<TicketType[]>([
        { value: "attraction", label: "Atrakcja", icon: "mdi-star" },
        { value: "bus", label: "Autobus", icon: "mdi-bus" },
        { value: "plane", label: "Samolot", icon: "mdi-airplane" },
        { value: "train", label: "Pociąg", icon: "mdi-train" },
    ]);

    const addTicket = (ticketData: Omit<Ticket, "id">) => {
        const newTicket: Ticket = {
            id: Date.now().toString(),
            type: ticketData.type,
            name: ticketData.name,
            date: ticketData.date,
            hour: ticketData.hour,
            file: ticketData.file,
        };
        if (ticketData.assignedTo && ticketData.assignedTo.trim() !== "") {
            newTicket.assignedTo = ticketData.assignedTo;
        }
        tickets.value.push(newTicket);
    };
    const createTicket = (file:File,data:Record<string, string>) =>{
        const {getTripId} = useUtilStore();
        console.log(file);
        console.log(data);
        console.log(getTripId('tripId').value);
       }

    return {
        tickets,
        ticketTypes,
        addTicket,
        createTicket
    };
});
