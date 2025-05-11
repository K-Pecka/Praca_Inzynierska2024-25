import { defineStore } from "pinia";
import { ref, watchEffect } from "vue";
import { fetchUserById } from "@/api";
import { getTripDetailsQuery, getExpensesQuery } from "@/api/services";
import { useUtilsStore } from "@/stores";

export const useMembersStore = defineStore("tripDetails", () => {
  const { getTripId } = useUtilsStore();

  const { data: trip, isLoading: isLoadingTrip } = getTripDetailsQuery(
    getTripId()
  );
  interface Member {
    name: string;
    userId: number;
    is_guest?: boolean;
    is_owner?: boolean;
    email: string;
  }
  const members = ref<Member[]>([]);

  const getUserById = async (id: number) => {
    const user = await fetchUserById(id);
    return {
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      userId: id,
    };
  };

  watchEffect(async () => {
    if (!getTripId()) return;

    const membersRaw = trip.value?.members ?? ([] as { id: number }[]);
    const pendingRaw = trip.value?.pending_members ?? ([] as { id: number }[]);

    const user = trip?.value?.creator?.id
      ? await getUserById(trip.value.creator.id)
      : null;

    const creator: Member = user
      ? { ...user, email: user.email ?? "unknown@example.com", is_owner: true, is_guest: false }
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
        return { ...user, email: user.email ?? "unknown@example.com", is_guest: false };
      })
    );

    const pending = await Promise.all(
      pendingRaw.map(async (entry) => {
        const id =
          typeof entry === "object" && entry !== null ? entry.id : entry;
        const user = await getUserById(id);
        return { ...user, email: user.email ?? "unknown@example.com", is_guest: true };
      })
    );

    const userMap = new Map<number, (typeof confirmed)[0]>();
    for (const user of [creator, ...pending, ...confirmed]) {
      userMap.set(user.userId, { ...user, is_guest: user.is_guest ?? false });
    }

    members.value = Array.from(userMap.values());
  });

  return {
    members,
    getUserById,
  };
});
