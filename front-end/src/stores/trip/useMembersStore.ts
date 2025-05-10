import { defineStore } from "pinia";
import {  ref, watchEffect } from "vue";
import { fetchUserById } from "@/api";
import { getTripDetailsQuery, getExpensesQuery } from "@/api/services";
import { useUtilsStore } from "@/stores";

export const useMembersStore = defineStore("tripDetails", () => {
  const {getTripId} = useUtilsStore();

  const { data: trip, isLoading: isLoadingTrip } = getTripDetailsQuery(getTripId());

  const members = ref<{ name: string; userId: number; is_guest: boolean }[]>([]);

  const getUserById = async (id: number) => {
    const user = await fetchUserById(id);
    //console.log(user);
    return {
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      userId: id,
    };
  };

  watchEffect(async () => {
    if (!getTripId()) return;

    const membersRaw = trip.value?.members ?? [] as { id: number }[];
    const pendingRaw = trip.value?.pending_members ?? [] as { id: number }[];
    
    const creator: { userId: number; name: string; email: string | undefined; is_guest: boolean } = trip?.value?.creator?.id 
      ? { ...(await getUserById(trip.value.creator.id)), is_guest: false }
      : { userId: -1, name: "Unknown", email: undefined, is_guest: false };

    const confirmed = await Promise.all(
      membersRaw.map(async (entry) => {
        const id = typeof entry === "object" && entry !== null ? entry.id : entry;
        const user = await getUserById(id);
        return { ...user, is_guest: false };
      })
    );

    const pending = await Promise.all(
      pendingRaw.map(async (entry) => {
        const id = typeof entry === "object" && entry !== null ? entry.id : entry;
        const user = await getUserById(id);
        return { ...user, is_guest: true };
      })
    );

    const userMap = new Map<number, typeof confirmed[0]>();
    for (const user of [creator,...pending, ...confirmed]) {
      if (user.userId === undefined) continue;
      userMap.set(user.userId, user);
    }

    members.value = Array.from(userMap.values());
  });

  return {
    members,
    getUserById,
  };
});
