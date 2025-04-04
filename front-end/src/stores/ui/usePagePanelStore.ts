import { defineStore } from "pinia";
import { RoleSelection, SideNavItem } from "@/type/interface";
import { image } from "@/lib";
import { usePermissionStore } from "@/stores";
import { useRoleStore } from "../auth/useRoleStore";
import { Role } from "@/type/enum";
export const usePagePanelStore = defineStore("pagePanel", () => {
    const { getRole } = useRoleStore();
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
                path:{name:"yourTripGuide"}
            },
        ],
    };

    const getSideNavItems = (tripId: string): SideNavItem[]=> {
        return getRole() == Role.GUIDE?[]:[
        {
            label: "Panel",
            icon: image.icon.menu.dashboard,
            name:"panel",
            route: { name: 'tripDashboard', params: { tripId:tripId }},
        },
        {
            label: "Plany",
            name:"plan",
            icon: image.icon.menu.plan,
            children: [
                { label: "Utworzone", route: { name: 'yourPlan', params: { tripId:tripId }} },
                { label: "Dodaj", route: { name: 'PlanForm', params: { tripId:tripId }} },
            ],
        },
        {
            label: "Bilety",
            name:"ticket",
            icon: image.icon.menu.ticket,
            route: { name: 'TicketsView', params: { tripId:tripId }},
        },
        {
            label: "Budżet",
            name:"budget",
            icon: image.icon.menu.budget,
            children: [
                { label: "Pokaż",name:"budgetShow", route: { name: 'ExpenseTracker', params: { tripId:tripId }} },
                { label: "zmień budżet",name:"budgetChange", route: { name: 'budget', params: { tripId:tripId }} },
            ],
        },
        {
            label: "Uczestnicy",
            name:"participant",
            icon: image.icon.menu.participant,
            route: { name: 'ParticipantsView', params: { tripId:tripId }},
        },
        {
            label: "Ustawienia",
            name:"setting",
            icon: image.icon.menu.setting,
            children: [
                { label: "Edycja wycieczki",name:"settingEdit", route: { name: 'TripEdit', params: { tripId:tripId }} },
            ],
        },
    ]};

    return {
        getRoleSelection,
        getSideNavItems,
    };
});