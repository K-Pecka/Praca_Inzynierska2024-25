import type { RouteRecordRaw } from "vue-router";
import InviteLayout from "@/layouts/InviteLayout.vue";
import InviteLanding from "@/views/invite/InviteLanding.vue";
const inviteRoutes = {
  path: "/trip",
  name: "tripInvite",
  component: InviteLayout,
  meta: { title: "Home" },
  children: [
    {
      path: "invite",
      name: "tripIntro",
      component: InviteLanding,
    },
  ],
};

export default inviteRoutes;
