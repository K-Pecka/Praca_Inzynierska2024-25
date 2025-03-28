import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import router from "@/router";
import { computed } from "vue";

export const useUtilStore = defineStore("utils", () => {
  const route = useRoute();
  const useRouter = () => router;
  const getTripId = () => {
    return computed<string>(() => {
      const tripId = route.params?.tripId;
      return Array.isArray(tripId) ? tripId[0] : tripId;
    });
  };
  const getCurrentPath = () => {
    name: route.name;
  };
  const isCurrentRouteNotInSet = (RouteSet: string[]) =>
    computed(() => {
      return !RouteSet.includes(route.name as string);
    });
  const formatDate = (date: Date) => {
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    };
    return new Intl.DateTimeFormat("pl-PL", options).format(date);
  };
  return { useRouter, getTripId, isCurrentRouteNotInSet, getCurrentPath,formatDate };
});
