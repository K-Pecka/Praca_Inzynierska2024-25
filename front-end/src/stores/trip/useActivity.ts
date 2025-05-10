import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useMutation, useQuery } from "@tanstack/vue-query";
import { createActivity } from "@/api/endpoints/trip/activity";
import { useNotificationStore } from "@/stores";
import { fetchActivityTypes } from "@/api/endpoints/trip/activity";
import { Activity, ActivityType } from "@/types/interface";
import {
  getActivitiesQuery,
} from "@/api/services/activityQuery";

export const useActivity = (tripIdFn: () => string | number | undefined,planIdFn: () => string | number | undefined) =>{
  const activities = ref<Activity[]>([]);
  const activeError = ref<boolean>(false);
  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
  const activityTypes = ref<ActivityType[]>([]);
  const resolvedTripId = () => String(tripIdFn?.() ?? "");
  const resolvedPlanId = () => String(planIdFn?.() ?? "");
  const getActivities = (tripId: string, planId: string) => {
    const {data: activities,isLoading: isLoading_activities,error: error_activities} = getActivitiesQuery((tripId ?? resolvedTripId()),(planId || resolvedPlanId()));
    return { activities, isLoading_activities, error_activities };
  }
        

  async function getErrorStatus(){
    return activeError.value;
  }
  async function setError(error:boolean){
    activeError.value=error;
  }
  function addActivity(
    activityData: Activity,
    param: Record<string, string> = {}
  ) {
    activityMutationAdd.mutate(
      { activityData, param },
    );
  }

  function removeActivity(activityId: number) {
    activities.value = activities.value.filter((a) => a.id !== activityId);
  }

  const activitiesByDate = computed(() => {
    return (date: string) => activities.value.filter((a) => a.date === date);
  });

  const activityMutationAdd = useMutation({
    mutationFn: ({
      activityData,
      param,
    }: {
      activityData: Activity;
      param: Record<string, string>;
    }) => createActivity(activityData, param),
    onSuccess: () => {
      setSuccessCurrentMessage("Dodano aktywność");
    },
    onError: () => {
        
        setError(true);
      
      setErrorCurrentMessage("Błąd podczas dodawania aktywności");
      
    },
  });

  async function loadActivityTypes(tripId: string) {
    const typesFromApi = await fetchActivityTypes(tripId);
    activityTypes.value = typesFromApi.map(t => ({
      id: t.id,
      name: t.name,
    }));
  }

  return {
    getErrorStatus,
    setError,
    activities,
    getActivities,
    activityTypes,
    addActivity,
    removeActivity,
    activitiesByDate,
    loadActivityTypes
  };
};
