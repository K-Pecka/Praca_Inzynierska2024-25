import { useQuery, UseQueryOptions } from "@tanstack/vue-query";
import { defineStore } from "pinia";
import { computed } from "vue";
import { useUserStore } from "./userStore";
import router from "@/router";

interface Button {
  title: string;
  class: String[];
  onclick: (id: number | undefined) => void;
}
export const useTripStore = defineStore("trip", () => {
  const { getToken } = useUserStore();

  const fetchTrips = async () => {
    const response = await fetch("https://api.plannder.com/trip/all/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`,
      },
    });

    if (!response.ok) {
      throw new Error("Błąd podczas pobierania wycieczek");
    }

    return response.json();
  };

  const deleteTrip = (id: number) => {
    alert(`Usuń wycieczkę o ID: ${id}`);
  };

  const getTrips = () => {
    return useQuery({
      queryKey: ["trips"],
      queryFn: fetchTrips,
    });
  };

  const yourTrips = computed(() => {
    return {btn: [
      {
        title: "Zarządzaj wycieczką",
        class:['primary'],
        onclick: (id: Number) => router.push(`planel/YourTrip/${id}`),
      },
      {
        title: "Zarządzaj wycieczką",
        class:['accent'],
        onclick: (id: number) => deleteTrip(id),
      },
    ],
    trips:getTrips
  }
});

  return { yourTrips };
});
