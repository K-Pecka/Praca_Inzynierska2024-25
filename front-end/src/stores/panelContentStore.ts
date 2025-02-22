import { defineStore } from "pinia";
import { RoleSelection, SideNavItem } from "@/type/interface";

export const usePagePanelStore = defineStore("pagePanel", () => {
    const getRoleSelection:RoleSelection = {
        title: "Witaj w aplikacji Plannder",
        subtitle: "W jakiej roli planujesz zorganizować podróż?",
        roles: [
            {
                title: "Turysta",
                description: "Planowanie indywidualnych podróży dla siebie i rodziny",
                image: "/picture/tourist.svg",
                path:{name:"yourTrip"}
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: "/picture/guide.svg",
                path:{name:"yourTrip"}
            },
        ],
    };
    const navbar = {
        accountIcon: "/picture/myAccount.svg",
    };

    const getsideNavItems = (tripId: string): SideNavItem[]=> [
        {
            label: "Panel",
            icon: "/picture/sideNav/panel.svg",
            route: { name: 'tripDashboard', params: { tripId:tripId }},
        },
        {
            label: "Plany",
            icon: "/picture/sideNav/plans.svg",
            children: [
                { label: "Utworzone", route: { name: 'yourPlan', params: { tripId:tripId }} },
                { label: "Dodaj", route: { name: 'PlanForm', params: { tripId:tripId }} },
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
                { label: "Pokaż", route: { name: 'ExpenseTracker', params: { tripId:tripId }} },
                { label: "zmień budżet", route: { name: 'budget', params: { tripId:tripId }} },
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
        getRoleSelection,
        navbar,
        getsideNavItems,
    };
});