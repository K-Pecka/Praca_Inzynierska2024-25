import { defineStore } from "pinia";

export const usePermissionStore = defineStore("permission", () => {
    const profile = {
        admin: 0,
        tourist: 1,
        touristPremium: 2,
        guide: 3,
      }
    const touristPanelNavAccess:Record<string,number[]> = {
        ticket:[0,2,3],
        budeget:[0,2,3],
        budgetShow:[0,2,3],
        budgetChange:[0,2,3],
        participant:[0,2,3]
    }
    const pathAccess:Record<string,number[]> = {
        budget:[0,2,3],
        TicketsView:[0,2,3],
        ExpenseTracker:[0,2,3],
        ParticipantsView:[0,2,3]
    }
    const access:Record<string,Record<string,number[]>> = {
        nav:touristPanelNavAccess,
        path:pathAccess
    }
    const goTo = () => ({name:"pricingSection"})
    const hasPermission = (profile: number[], name: string | undefined, type: "nav" | "path" = "nav"): boolean => {
        const allowedProfiles = access[type]?.[name || ''];
        if (!allowedProfiles) return true;
        return true//profile.some((p) => allowedProfiles.includes(p));
      };
    return {hasPermission,goTo}
});
