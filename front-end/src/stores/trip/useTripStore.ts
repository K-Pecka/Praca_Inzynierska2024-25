import {
  useMutation,
  useQuery,
  useQueryClient
} from "@tanstack/vue-query";
import { defineStore } from "pinia";
import { computed } from "vue";
import { useAuthStore,useNotificationStore } from "@/stores";
import router from "@/router";
import { fetchTrips, fetchTrip, deleteTrip, createTrip } from "@/api";
import { fetchPlans, createPlan } from "@/api";
import { saveBudget } from "@/api";
import { Plan } from "@/type";

export const useTripStore = defineStore("trip", () => {
  const queryClient = useQueryClient();

  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
    
  const deleteTripMutation = useMutation({
    mutationFn: deleteTrip,
    onSuccess: () => {
      setSuccessCurrentMessage("Pomyślnie usunięto wycieczkę");
      queryClient.invalidateQueries({ queryKey: ["trips"] });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message);
    },
  });
  const handleDeleteTrip = async (id: string) => {
    try {
      console.log("Deleting trip with id:", id);
      await deleteTripMutation.mutateAsync({ tripId: id });
    } catch (err) {
      console.error("Failed to delete trip:", err);
    }
  };

  const getTripDetails = (id: string) => {
    return useQuery({
      queryKey: ["trip", id],
      queryFn: () => fetchTrip({ tripId: id }),
    });
  };
const getDashboard = (id: string) => {
  const { data: tripRaw, isLoading, error } = getTripDetails(id);
  const tripTime = computed(
    () => `${tripRaw.value?.start_date ?? "..."} - ${tripRaw.value?.end_date ?? "..."}`
  );
  const budget = computed(() => `${tripRaw.value?.budget?.amount ?? "..."} PLN`);
  const participantCount = computed(
    () => `${tripRaw.value?.members?.length ?? "..."} Uczestników`
  );
  const activityCount = computed(() => "0 Aktywności");
  const upcomingActivities = computed(() => []);
  const boxes = computed(() => [
    {
      title: "Czas trwania",
      icon:"mdi-calendar-month-outline",
      content: tripTime.value,
      set: {
        order: 1,
        size: {
          sm: { col: 12, row: 1 },
          md: { col: 6, row: 1 },
          lg: { col: 3, row: 1 },
        },
      },
    },
    {
      title: "Budżet",
      icon:"mdi-currency-usd",
      content: budget.value,
      set: {
        order: 2,
        size: {
          sm: { col: 12, row: 1 },
          md: { col: 6, row: 1 },
          lg: { col: 3, row: 1 },
        },
      },
    },
    {
      title: "Uczestnicy",
      icon:"mdi-account-multiple",
      content: participantCount.value,
      set: {
        order: 3,
        size: {
          sm: { col: 12, row: 1 },
          md: { col: 6, row: 1 },
          lg: { col: 3, row: 1 },
        },
      },
    },
    {
      title: "Aktywności",
      icon:"mdi-clock-outline",
      content: activityCount.value,
      set: {
        order: 4,
        size: {
          sm: { col: 12, row: 1 },
          md: { col: 6, row: 1 },
          lg: { col: 3, row: 1 },
        },
      },
    },
    {
      title: "Nadchodzące aktywności",
      icon:"mdi-timer-refresh-outline",
      content: upcomingActivities.value,
      set: {
        order: 5,
        size: {
          sm: { col: 12, row: 2 },
          md: { col: 6, row: 2 },
          lg: { col: 6, row: 2 },
        },
      },
    },
    {
      title: "Ważne informacje",
      icon:"mdi-information-outline",
      content: upcomingActivities.value,
      set: {
        order: 5,
        size: {
          sm: { col: 12, row: 2 },
          md: { col: 6, row: 2 },
          lg: { col: 6, row: 2 },
        },
      },
    },
  ]);
  return { boxes, isLoading, error };
};
  const getPlans = (id: string) => {
    return useQuery({
      queryKey: ["plans", id],
      queryFn: () => fetchPlans({ tripId: id }),
    });
  };
  const getTrips = () => {
    return useQuery({
      queryKey: ["trips"],
      queryFn: fetchTrips,
    });
  };
  const yourTrips = computed(() => {
    return {
      btn: [
        {
          title: "Zarządzaj wycieczką",
          class: ["primary"],
          onclick: (id: string) =>
            router.push(`/panel/YourTrip/${id}`),
        },
        {
          title: "usuń wycieczkę",
          class: ["accent"],
          onclick: (id: string) => handleDeleteTrip(id),
        },
      ],
      trips: getTrips,
    };
  });
  const yourPlans = computed(() => {
    return {
      btn: [
        {
          title: "Zarządzaj planem",
          class: ["primary"],
          onclick: (trip: string, id: string) => router.push(`/panel/YourTrip/${id}`),
        },
        {
          title: "usuń plan",
          class: ["accent"],
          onclick: (id: string) => handleDeleteTrip(id),
        },
      ],
      plans: getPlans,
    };
  });
  const tripMutationBudget = useMutation({
    mutationFn: saveBudget,
    onSuccess: (data) => {
      setSuccessCurrentMessage("zapisano");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  const planMutationAdd = useMutation({
    mutationFn: ({ data, tripId }: { data: Plan; tripId: string }) =>
      createPlan(data, { tripId: tripId }),
    onSuccess: (data) => {
      router.back();
      setSuccessCurrentMessage("dodano planu");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  const tripMutationAdd = useMutation({
    mutationFn: createTrip,
    onSuccess: (data) => {
      router.back();
      setSuccessCurrentMessage("dodano wycieczkę");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  return {
    getDashboard,
    yourTrips,
    yourPlans,
    getTripDetails,
    tripMutationAdd,
    tripMutationBudget,
    planMutationAdd,
  };
});
