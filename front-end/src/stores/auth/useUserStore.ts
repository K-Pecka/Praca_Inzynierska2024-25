import { defineStore } from 'pinia';
import {fetchUserById} from '@/api';
import { useQuery } from '@tanstack/vue-query';
import {User} from '@/types';
export const useUserStore = defineStore('user', () => {

  const getUserById = (id: number) => {
    return useQuery<User, Error>({
        queryKey: ["user",id],
        queryFn: ({ queryKey }) => fetchUserById(queryKey[1] as number),
    })
  };
  return { getUserById };
});