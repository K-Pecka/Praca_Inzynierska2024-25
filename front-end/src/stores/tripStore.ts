import {
  useMutation,
  useQuery,
  useQueryClient,
  UseQueryOptions,
} from "@tanstack/vue-query";
import { defineStore } from "pinia";
import { computed } from "vue";
import { useAuthStore } from "./auth/useAuthStore";
import router from "@/router";
import { useNotificationStore } from "./ui/useNotificationStore";
import { fetchTrips, fetchTrip, deleteTrip, createTrip } from "@/api";
import { fetchPlans, createPlan } from "@/api";
import { saveBudget } from "@/api";
import { Plan } from "@/type";

export const useTripStore = defineStore("trip", () => {
  const queryClient = useQueryClient();

  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useNotificationStore();
  const { getToken } = useAuthStore();

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
          onclick: (trip: string, id: string) =>
            router.push(`/panel/YourTrip/${trip}`),
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
          title: "Zarządzaj wycieczką",
          class: ["primary"],
          onclick: (id: string) => router.push(`/panel/YourTrip/${id}`),
        },
        {
          title: "usuń wycieczkę",
          class: ["accent"],
          onclick: (id: string) => handleDeleteTrip(id),
        },
      ],
      plans: getPlans,
    };
  });
  // const saveBudget = async (data: {
  //   amount: string;
  //   currency: string;
  //   trip: Number;
  // }) => {
  //   const response = await fetch(
  //     `https://api.plannder.com/trip/${data.trip}/budget/update/`,
  //     {
  //       method: "PATCH",
  //       headers: {
  //         "Content-Type": "application/json",
  //         Authorization: `Bearer ${getToken()?.access}`,
  //       },
  //       body: JSON.stringify(data),
  //     }
  //   );
  //   console.log(data);
  //   if (!response.ok) {
  //     const errorData = await response.json();
  //     console.log(errorData);
  //     throw new Error(errorData || "unknow");
  //   }

  //   return response.json();
  // };
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
    yourTrips,
    yourPlans,
    getTripDetails,
    tripMutationAdd,
    tripMutationBudget,
    planMutationAdd,
  };
});
