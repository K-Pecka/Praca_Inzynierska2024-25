import { Role } from "@/type/enum";
import type { PiniaPluginContext } from "pinia";
import { useRoleStore } from "@/stores/auth/useRoleStore";

export function piniaBasePlugin({ store }: PiniaPluginContext) {

  store.initialize = (payload: string) => {
    const { setRole } = useRoleStore();
    setRole(payload);
  };

  const initialState = JSON.parse(JSON.stringify(store.$state));
  store.reset = () => {
    store.$patch(initialState);
  };
  store.$subscribe((_, state) => {
    localStorage.setItem(`store:${store.$id}`, JSON.stringify(state));
  });

  const saved = localStorage.getItem(`store:${store.$id}`);
  if (saved) {
    store.$patch(JSON.parse(saved));
  }
}
