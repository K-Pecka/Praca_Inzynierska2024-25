import { defineStore } from "pinia";
export const useMessageStore = defineStore("message", () => {
    const errorMessage = {
        default:{
            response: "nie znany błąd"
        },
        login:{
            response: "Błąd logowania",
        }
    }
    const responseError = (type: keyof typeof errorMessage) => errorMessage[type]?.response || errorMessage.default.response
    return {responseError};
});