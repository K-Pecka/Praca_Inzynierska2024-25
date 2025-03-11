import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import { computed } from "vue";

export const useUtilStore = defineStore("utils", () => {
    const route = useRoute();
    const getTripId = (paramName: string) => computed(() => route.params[paramName]);
    const getCurrentPath = () =>{name:route.name}
    const isCurrentRouteNotInSet = (RouteSet: string[]) => computed(() => {
        return !RouteSet.includes(route.name as string)
    });
    return {getTripId,isCurrentRouteNotInSet,getCurrentPath}
})
