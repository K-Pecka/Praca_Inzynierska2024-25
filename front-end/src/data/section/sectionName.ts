import { Role } from "@/types/enum";

export const sectionDashboard = (role:Role) => {
    switch (role) {
        case Role.TOURIST:
            return "Twoje ostatnie wydatki";
        case Role.GUIDE:
            return "Ostatnie zaległości uczestników";
        default:
            return "Nieznana rola";
    }
}
