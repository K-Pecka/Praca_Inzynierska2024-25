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
                path:"panel/YourTrip"
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: "/picture/guide.svg",
                path:"/"
            },
        ],
    };
    const navbar = {
        accountIcon: "/picture/myAccount.svg",
    };

    const sideNavItems = [
        {
            label: "Panel",
            icon: "/picture/sideNav/panel.svg",
            route: "/panel/trip",
        },
        {
            label: "Plany",
            icon: "/picture/sideNav/plans.svg",
            children: [
                { label: "Utworzone", route: "/" },
                { label: "Dodaj", route: "/" },
            ],
        },
        {
            label: "Bilety",
            icon: "/picture/sideNav/tickets.svg",
            children: [
                { label: "Dodane", route: "/" },
                { label: "Dodaj", route: "/" },
            ],
        },
        {
            label: "Budżet",
            icon: "/picture/sideNav/budget.svg",
            children: [
                { label: "?", route: "/" },
                { label: "?", route: "/" },
            ],
        },
        {
            label: "Uczestnicy",
            icon: "/picture/sideNav/participants.svg",
            children: [
                { label: "?", route: "/" },
                { label: "?", route: "/" },
            ],
        },
        {
            label: "Ustawienia",
            icon: "/picture/sideNav/settings.svg",
            children: [
                { label: "?", route: "/" },
                { label: "?", route: "/" },
            ],
        },
    ];

    return {
        roleSelection,
        navbar,
        sideNavItems,
    };
});