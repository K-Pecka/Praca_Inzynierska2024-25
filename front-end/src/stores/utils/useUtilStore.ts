import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import router from "@/router";
import { computed } from "vue";

export const useUtilStore = defineStore("utils", () => {
    const route = useRoute();
    const useRouter = () => router
    const getTripId = (paramName: string) => computed(() => route.params[paramName]);
    const getCurrentPath = () =>{name:route.name}
    const isCurrentRouteNotInSet = (RouteSet: string[]) => computed(() => {
        return !RouteSet.includes(route.name as string)
    });
    return {useRouter,getTripId,isCurrentRouteNotInSet,getCurrentPath}
})
