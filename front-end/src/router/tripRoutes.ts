import Dashboard from "@/views/panel/YourTrip.vue";
import {RoleSelection as roleSelection, TripForm} from "@/views/panel";
import ChooseRoleLayout from "@/layouts/ChooseRoleLayout.vue";

const tripRoutes = {
    path: "/role",
    name: "chooseRole",
    component: ChooseRoleLayout,
    children: [
        {
            path: "/:role/choose-trip",
            name: "ChooseTrip",
            component: Dashboard,
            meta: {requiresAuth: true},
        },
        {
            path: "/role-selection",
            name: "roleSelection",
            component: roleSelection
        },
        {
            path: "/:role/trip/create",
            name: "createTrip",
            component: TripForm
        },
    ]
};

export default tripRoutes;