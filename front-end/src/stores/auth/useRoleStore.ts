import { defineStore } from 'pinia';
import { Role } from '@/type/enum';
import { ref } from 'vue';

export const useRoleStore = defineStore('roleStore', () => {
  const role = ref<Role>(Role.UNKNOWN);

  const setRole = (newRole: string) => {
    let roleValue:Role = Role.UNKNOWN;
    console.warn("setRole",newRole);
    if (newRole.toLowerCase().includes(Role.GUIDE.toLowerCase())){
        roleValue = Role.GUIDE;
    }
    else{
        roleValue = Role.TURIST;
    }
    role.value = roleValue;
  };
  const getRole = () => role.value;

  return { getRole, setRole };
});