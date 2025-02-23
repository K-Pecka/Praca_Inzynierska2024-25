import { defineStore } from "pinia";
import { RoleSelection, SideNavItem } from "@/type/interface";
import { image } from "@/lib";
export const usePagePanelStore = defineStore("pagePanel", () => {
    const getRoleSelection:RoleSelection = {
        title: "Witaj w aplikacji Plannder",
        subtitle: "W jakiej roli planujesz zorganizować podróż?",
        roles: [
            {
                title: "Turysta",
                description: "Planowanie indywidualnych podróży dla siebie i rodziny",
                image: image.role.turist,
                path:{name:"yourTrip"}
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: image.role.guide,
                path:{name:"yourTrip"}
            },
        ],
    };
    const navbar = {
        accountIcon: "/picture/myAccount.svg",
    };

    const getSideNavItems = (tripId: string): SideNavItem[]=> [
        {
            label: "Panel",
            icon: image.icon.menu.dashboard,
            route: { name: 'tripDashboard', params: { tripId:tripId }},
        },
        {
            label: "Plany",
            icon: image.icon.menu.plan,
            children: [
                { label: "Utworzone", route: { name: 'yourPlan', params: { tripId:tripId }} },
                { label: "Dodaj", route: { name: 'PlanForm', params: { tripId:tripId }} },
            ],
        },
        {
            label: "Bilety",
            icon: image.icon.menu.ticket,
            children: [
                { label: "Dodane", route: "/" },
                { label: "Dodaj", route: "/" },
            ],
        },
        {
            label: "Budżet",
            icon: image.icon.menu.budget,
            children: [
                { label: "Pokaż", route: { name: 'ExpenseTracker', params: { tripId:tripId }} },
                { label: "zmień budżet", route: { name: 'budget', params: { tripId:tripId }} },
            ],
        },
        {
            label: "Uczestnicy",
            icon: image.icon.menu.participant,
            children: [
                { label: "?", route: "/" },
                { label: "?", route: "/" },
            ],
        },
        {
            label: "Ustawienia",
            icon: image.icon.menu.setting,
            children: [
                { label: "?", route: "/" },
                { label: "?", route: "/" },
            ],
        },
    ];

    return {
        getRoleSelection,
        navbar,
        getSideNavItems,
    };
});