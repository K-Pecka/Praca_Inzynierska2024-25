import { Role } from "@/types/enum";

export const sectionDashboard = (role:Role,isOwner: boolean) => {
    if(role == Role.TOURIST) return "Twoje ostatnie wydatki"
    if(role == Role.GUIDE && isOwner)return "Ostatnie zaległości uczestników";
    if(role == Role.GUIDE && !isOwner)return "Ostatnie zaległości"
}
