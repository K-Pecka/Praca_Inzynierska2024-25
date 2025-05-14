import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { createActivity } from "@/api/endpoints/trip/activity";
import { useNotificationStore, useUtilsStore } from "@/stores";
import { fetchActivity, fetchActivityTypes } from "@/api/endpoints/trip/activity";
import { Activity, ActivityType } from "@/types/interface";
import {getMutationDelete} from "@/api/services/activityQuery"

export const useActivityStore = defineStore("activity", () => {
  const {getPlanId,getTripId} = useUtilsStore()
  const notification = useNotificationStore();
  const activities = ref<Activity[]>([]);
  const activeError = ref<boolean>(false);
  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
  const queryClient = useQueryClient();
  const activityTypes = ref<ActivityType[]>([]);

  const getActivity = (tripId?: number, planId?: number) => {
    return useQuery<Activity[], Error>({
      queryKey: ["activities", (tripId || getTripId()), (planId || getPlanId())],
      queryFn: () => fetchActivity({ tripId: String(tripId || getTripId()), planId: String(planId || getPlanId()) }),
    });
  };

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
  const deleteActivity = getMutationDelete({
          queryClient,
          notification,
          successMessage: "Pomyślnie usunięto aktywność",
          errorMessage: "Nie udało się usunąć aktywności",
      })

  // Grupowanie aktywności po dacie
  const activitiesByDate = computed(() => {
    return (date: string) => activities.value.filter((a) => a.date === date);
  });

  // Mutacja do dodawania aktywności
  const activityMutationAdd = useMutation({
    mutationFn: ({
      activityData,
      param,
    }: {
      activityData: Activity;
      param: Record<string, string>;
    }) => createActivity(activityData, param),
    onSuccess: (_, variables) => {
      setSuccessCurrentMessage("Dodano aktywność");
      queryClient.invalidateQueries({ queryKey: ["activities", Number(variables.param.tripId), Number(variables.param.planId)] });
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
    getActivity,
    activityTypes,
    addActivity,
    activitiesByDate,
    loadActivityTypes,
    deleteActivity
  };
});
