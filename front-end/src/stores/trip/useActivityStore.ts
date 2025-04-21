import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useMutation, useQuery } from "@tanstack/vue-query";
import { createActivity } from "@/api/endpoints/trip/activity";
import { useNotificationStore } from "@/stores";
import { fetchActivity } from "@/api/endpoints/trip/activity";
import router from "@/router";

export interface Activity {
  id: number;
  type: string;
  name: string;
  date: string;
  start_time: string;
  duration: string;
  location?: string;
  assignedTo?: string;
  description?: string;
}

interface ActivityType {
  value: string;
  label: string;
  icon: string;
}

export const useActivityStore = defineStore("activity", () => {
  const activities = ref<Activity[]>([]);
  const activeError = ref<boolean>(false);
  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
  const activityTypes = ref<ActivityType[]>([
    { value: "tour", label: "Zwiedzanie", icon: "mdi-binoculars" },
    { value: "food", label: "Jedzenie", icon: "mdi-food" },
    { value: "sport", label: "Sport", icon: "mdi-basketball" },
    { value: "relax", label: "Relaks", icon: "mdi-beach" },
  ]);
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
    onSuccess: () => {
      setSuccessCurrentMessage("Dodano aktywność");
    },
    onError: () => {
        console.log(activeError.value);
        setError(true);
        console.log(activeError.value);
      setErrorCurrentMessage("Błąd podczas dodawania aktywności");
      
    },
  });

  return {
    getErrorStatus,
    setError,
    activities,
    getActivity,
    activityTypes,
    addActivity,
    removeActivity,
    activitiesByDate,
  };
});
