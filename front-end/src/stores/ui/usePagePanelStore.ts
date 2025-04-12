import { defineStore } from "pinia";
import { RoleSelection, SideNavItem } from "@/type/interface";
import { image } from "@/lib";
import { useRoleStore } from "../auth/useRoleStore";
import { Role } from "@/type/enum";
import { getGudieNav,getTouristNav } from "@/dataStorage/page/panel";

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
    const selectRole:Record<Role, (tripId:string) => SideNavItem[]>={
        [Role.GUIDE]: getGudieNav,
        [Role.TURIST]: getTouristNav,
        [Role.UNKNOWN]: function (): SideNavItem[] {
            throw new Error("Function not implemented.");
        },
        [Role.ADMIN]: function (): SideNavItem[] {
            throw new Error("Function not implemented.");
        }
    }
    const getSideNavItems = (tripId: string): SideNavItem[]=> 
        selectRole[getRole()](tripId) || [];
    
    return {
        getRoleSelection,
        getSideNavItems,
    };
});