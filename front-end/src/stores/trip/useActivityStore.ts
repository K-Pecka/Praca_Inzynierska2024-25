import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { createActivity } from "@/api/endpoints/trip/activity";
import { useNotificationStore } from "@/stores";
import { fetchActivity, fetchActivityTypes } from "@/api/endpoints/trip/activity";
import { Activity, ActivityType } from "@/types/interface";


export const useActivityStore = defineStore("activity", () => {
  const activities = ref<Activity[]>([]);
  const activeError = ref<boolean>(false);
  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
  const queryClient = useQueryClient();
  const activityTypes = ref<ActivityType[]>([]);

  //   const fetchActivity = async() => {
  //     return [
  //       {
  //         id: 1,
  //         name: "string",
  //         type: "string",
  //         date: "07-04-2025",
  //         description: "string",
  //         location: "string",
  //         start_time: "09:00:00",
  //         duration: "0",
  //       },
  //       {
  //         id: 3,
  //         name: "string",
  //         type: "string",
  //         date: "2025-04-07",
  //         description: "string",
  //         location: "string",
  //         start_time: "09:00:00",
  //         duration: "0",
  //       },
  //       {
  //         id: 2,
  //         name: "TEST_221209042025",
  //         type: "Zwiedzanie",
  //         date: "2025-04-07",
  //         description: "Test",
  //         location: "Madryt",
  //         start_time: "00:15:00",
  //         duration: "15",
  //       },
  //     ];
  //   };
  const getActivity = (tripId: string, itineraryId: string) => {
    return useQuery<Activity[], Error>({
      queryKey: ["activities", tripId, itineraryId],
      queryFn: () => fetchActivity({ tripId: tripId, planId: itineraryId }),
    });
  };
  // Gdy dane są załadowane, zapisujemy je do `activities`
  // Funkcja do dodawania aktywności
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

  // Funkcja do usuwania aktywności
  function removeActivity(activityId: number) {
    activities.value = activities.value.filter((a) => a.id !== activityId);
  }

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
      queryClient.invalidateQueries({ queryKey: ["activities", variables.param.tripId, variables.param.planId] });
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
    removeActivity,
    activitiesByDate,
    loadActivityTypes
  };
});
