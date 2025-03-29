import { defineStore } from "pinia";

export const usePermissionStore = defineStore("permission", () => {
    
    const touristPanelNavAccess:Record<string,number[]> = {
        ticket:[0,2,3],
        budeget:[0,2,3],
        budgetShow:[0,2,3],
        budgetChange:[0,2,3],
        participant:[0,2,3]
    }
    const goTo = () => ({name:"pricingSection"})
    const hasPermission = (profile: number[], name: string | undefined): boolean => {
        const allowedProfiles = touristPanelNavAccess[name || ''];
        console.log(profile)
        if (!allowedProfiles) return true;
        
        return profile.some((p) => allowedProfiles.includes(p));
      };
    return {touristPanelNavAccess,hasPermission,goTo}
});
