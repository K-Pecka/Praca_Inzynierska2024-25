import { defineStore } from 'pinia';
import { Role } from '@/types/enum';
import { ref} from 'vue';
import { useQueryClient } from "@tanstack/vue-query";
import { useRoute } from "vue-router";
import { getRoleQuery } from '@/api/services/roleQuery';

export const useRoleStore = defineStore('roleStore', () => {
  const role = ref<Role>(Role.UNKNOWN);
  const route = useRoute();
  const queryClient = useQueryClient();

  const switchRole = (role?:string) => getRoleQuery(role || String(route.params.role)); 

  const setRole = (newRole: string) => {
    let roleValue: Role = Role.UNKNOWN;

    if (newRole.toLowerCase().includes(Role.GUIDE.toLowerCase())) {
      roleValue = Role.GUIDE;
    } else {
      roleValue = Role.TOURIST;
    }

    if (role.value !== roleValue) {
      role.value = roleValue;
      queryClient.removeQueries({ queryKey: ['trips'] });
      queryClient.invalidateQueries({ queryKey: ['trips'] });
    }
  };

  const getRole = () => role.value;

  return {
    getRole,
    setRole,
    switchRole,
  };
},
  {
    persist: {
      key: 'role',
      storage: localStorage
    },
  });
