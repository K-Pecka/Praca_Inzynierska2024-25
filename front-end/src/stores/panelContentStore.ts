import { defineStore } from "pinia";

export const usePanelContentStore = defineStore("panelContent", () => {
    const roleSelection = {
        title: "Witaj w aplikacji Plannder",
        subtitle: "W jakiej roli planujesz zorganizować podróż?",
        roles: [
            {
                title: "Turysta",
                description: "Planowanie indywidualnych podróży dla siebie i rodziny",
                image: "/picture/tourist.svg",
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: "/picture/guide.svg",
            },
        ],
    };
    const navbar = {
        accountIcon: "/picture/myAccount.svg",
    };


    return {
        roleSelection,
        navbar,
    };
});