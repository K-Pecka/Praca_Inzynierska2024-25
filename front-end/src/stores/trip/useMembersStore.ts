import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useQueryClient } from "@tanstack/vue-query";
import type { Trip, User } from "@/types";
import { fetchUserById } from "@/api";

export const useMembersStore = defineStore("tripDetails", () => {
  const route = useRoute();
  const queryClient = useQueryClient();

  const members = ref<User[]>([]);

  const getUserById = async (id: number) => {
    const user = await fetchUserById(id);
    return {
      name: user.first_name ? `${user.first_name} ${user.last_name}` : null,
      email: user.email,
      userId: id,
    };
  };
  const trip = ref<Trip | null>(null);
  const setData = (data: Trip) => (trip.value = data);
  watch(
    trip,
    async () => {
      const cachedTrip: Trip | null = trip.value;
      if (!cachedTrip) {
        members.value = [];
        return;
      }

      const membersRaw = cachedTrip.members ?? ([] as { id: number }[]);
      const pendingRaw = cachedTrip.pending_members ?? ([] as { id: number }[]);

      const user = cachedTrip.creator?.id
        ? await getUserById(cachedTrip.creator.id)
        : null;

      const creator: User = user
        ? {
            ...user,
            email: user.email ?? "unknown@example.com",
            is_owner: true,
            is_guest: false,
          }
        : {
            userId: -1,
            name: "Unknown",
            email: "unknown@example.com",
            is_owner: true,
            is_guest: false,
          };

      const confirmed = await Promise.all(
        membersRaw.map(async (entry) => {
          const id =
            typeof entry === "object" && entry !== null ? entry.id : entry;
          const user = await getUserById(id);
          return {
            ...user,
            email: user.email ?? "unknown@example.com",
            name: user.name ?? "Turysta",
            is_guest: false,
          };
        })
      );

      const pending = await Promise.all(
        pendingRaw.map(async (entry) => {
          const id =
            typeof entry === "object" && entry !== null ? entry.id : entry;
          const user = await getUserById(id);
          return {
            ...user,
            name: user.name ?? "Gość",
            email: user.email ?? "unknown@example.com",
            is_guest: true,
          };
        })
      );

      const userMap = new Map<number, User>();
      for (const user of [creator, ...pending, ...confirmed]) {
        userMap.set(user.userId, {
          ...user,
          is_guest: user.is_guest ?? false,
        });
      }

      members.value = Array.from(userMap.values());
    },
    { immediate: true }
  );

  return {
    setData,
    members,
    getUserById,
  };
});
