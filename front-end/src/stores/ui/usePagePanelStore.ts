import { defineStore } from "pinia";
import { RoleSelection, SideNavItem } from "@/types/interface";
import { images } from "@/data";
import { useRoleStore } from "../auth/useRoleStore";
import { Role } from "@/types/enum";
import { getGudieNav,getTouristNav } from "@/data/page/panel";

export const usePagePanelStore = defineStore("pagePanel", () => {
    const { getRole } = useRoleStore();
    const getRoleSelection:RoleSelection = {
        title: "Witaj w aplikacji Plannder",
        subtitle: "W jakiej roli planujesz zorganizować podróż?",
        roles: [
            {
                title: "Turysta",
                description: "Planowanie indywidualnych podróży dla siebie i rodziny",
                image: images.role.tourist,
                path:{name:"ChooseTrip",params:{role:"tourist"}}
            },
            {
                title: "Przewodnik",
                description: "Tworzenie i zarządzanie wycieczkami dla grup turystycznych",
                image: images.role.guide,
                path:{name:"ChooseTrip",params:{role:"guide"}}
            },
        ],
    };
    const selectRole:Record<Role, () => SideNavItem[]>={
        [Role.GUIDE]: getGudieNav,
        [Role.TURIST]: getTouristNav,
        [Role.UNKNOWN]: function (): SideNavItem[] {
            throw new Error("Function not implemented.");
        },
        [Role.ADMIN]: function (): SideNavItem[] {
            throw new Error("Function not implemented.");
        }
    }
    const getSideNavItems = (): SideNavItem[]=> {
        return selectRole[getRole()]() || [];
    }
    return {
        getRoleSelection,
        getSideNavItems,
    };
});