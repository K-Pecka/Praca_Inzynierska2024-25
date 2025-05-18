import { useQuery } from "@tanstack/vue-query"
import { fetchUserRole } from "@/api/endpoints/auth";
import { computed } from "vue";

export const getRoleQuery= (role:string) => useQuery({
    queryKey: ['role'],
    queryFn: () => fetchUserRole(role),
    enabled: computed(() =>  role != '' && !!role && role !== 'undefined')
  });