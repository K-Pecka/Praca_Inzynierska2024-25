import {reactive} from "vue";

export const panelContentStore = reactive({
    roleSelection: {
        title: "Witaj w aplikacji Plannnder",
        subtitle: "W jakiej roli planujesz zorganizować podróż?",
        roles: [
            {
                title: "Turysta",
                description: "Planowanie indywidualnego planu podróży dla siebie i rodziny",
                image: "./picture/tourist.svg",
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: "./picture/p1.svg",
            },
        ],
    },
});