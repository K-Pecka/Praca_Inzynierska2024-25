import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import router from "@/router";
import { computed } from "vue";
import { budget } from "@/data/category/budget";
export const useUtilsStore = defineStore("utils", () => {
  const route = useRoute();
  const useRouter = () => router;
  const getTripId = ()=>{
    const id = route.params.tripId;
      return Number(Array.isArray(id) ? id[0] : id);
  }
  const getItineraryId = ()=>{
    const id = route.params.itineraryId;
      return Number(Array.isArray(id) ? id[0] : id);
  }
  const getRole = ()=>{
    const role = route.params.role;
      return String(Array.isArray(role) ? role[0] : role);
  }
  const getPage = () =>{
    const page = route.query.page;
    return Number(Array.isArray(page) ? page[0] : page) || 1;
  }
  const setPage = (newPage:number) =>{
    router.push({
    query: {
      ...route.query,
      page: newPage.toString(),
    },
  });
  }
  const isCurrentRouteNotInSet = (RouteSet: string[]) =>
    computed(() => {
      return !RouteSet.includes(route.name as string);
    });
  function formatDatePolish(date: string | Date): string {
    const parsed = typeof date === 'string' ? new Date(date) : date;

    if (isNaN(parsed.getTime())) {
      return 'Nieprawidłowa data';
    }

    return parsed.toLocaleDateString('pl-PL', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  }
  const mapCategoryBudget = (categoryId: number) => {
    const category = budget.find((cat: any) => cat.id === categoryId);
    if (category) {
      return {
        name: category.name,
        icon: category.icon
      };
    }
    return {
      name: "Unknown",
      icon: "mdi-help-circle-outline"
    };
  };
  const  combineDateAndTime = (date: string, time: string): string => {

    const dateTimeString = `${date}T${time}Z`;
  
    const dateTime = new Date(dateTimeString);
  
    if (isNaN(dateTime.getTime())) {
      throw new Error("Nieprawidłowa data lub czas");
    }

    return dateTime.toISOString();
  }
  const safeDivision = (numerator: number, denominator: number, percent: boolean) => {
    if (denominator === 0) {
      return 0;
    }
    if(percent) {
      return ((numerator / denominator) * 100).toFixed(2);
    }
    return (numerator / denominator).toFixed(2);
  };
  return {setPage,getPage,getItineraryId,getRole,safeDivision,combineDateAndTime,mapCategoryBudget,useRouter, getTripId, isCurrentRouteNotInSet, formatDatePolish };
});
