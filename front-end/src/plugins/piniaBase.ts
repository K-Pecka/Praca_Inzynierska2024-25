import type { PiniaPluginContext } from "pinia";
import { useRoleStore } from "@/stores/auth/useRoleStore";
import { useRoute } from "vue-router";
export function piniaBasePlugin({ store }: PiniaPluginContext) {

  store.initialize = () => {
    const { setRole } = useRoleStore();
    setRole(String(useRoute().params.role) || '');
  };
}
