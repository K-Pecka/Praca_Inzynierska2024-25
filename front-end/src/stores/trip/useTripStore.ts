import {
  useMutation,
  useQuery,
  useQueryClient
} from "@tanstack/vue-query";
import { defineStore } from "pinia";
import { computed } from "vue";
import { useNotificationStore } from "@/stores";
import router from "@/router";
import { fetchTrips, fetchTrip, deleteTrip, createTrip, updateTrip } from "@/api";
import { fetchPlans, createPlan,deleteItinerary } from "@/api";
import {fetchAddParticipant,fetchRemoveParticipant} from "@/api";
import { saveBudget } from "@/api";
import { Plan } from "@/type";
import type { Trip } from "@/type/interface";
import { useRoleStore } from "../auth/useRoleStore";
import { Role } from "@/type/enum";

export const useTripStore = defineStore("trip", () => {
  const queryClient = useQueryClient();
  const {getRole} = useRoleStore();
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
  const deleteItineraryMutation = useMutation({
    mutationFn:
    ({ tripId, planId }: { tripId: string; planId: string }) =>
      deleteItinerary({tripId, planId}),
    onSuccess: (data) => {
      setSuccessCurrentMessage(`Pomyślnie usunięto plan`);
      
      queryClient.invalidateQueries({ queryKey: ["plans",data?.tripId] });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message);
    },
  });
  const handleDeleteItinerary = async (Tripid: string,planId: string) => {
    
    try {
      await deleteItineraryMutation.mutateAsync({ tripId: Tripid, planId:planId });
    } catch (err) {
    }
  };
  const handleDeleteTrip = async (id: string) => {
    try {
      await deleteTripMutation.mutateAsync({ tripId: id });
    } catch (err) {
    }
  };

  const getTripDetails = (id: string) => {
    return useQuery<Trip>({
      queryKey: ["trip", id],
      queryFn: () => fetchTrip({ tripId: id }),
      //keepPreviousData: true,
    });
  };
  const getDashboard = (id: string) => {
    const { data: tripRaw, isLoading, error } = getTripDetails(id);
  
    const tripTime = computed(() => {
      if (tripRaw.value) {
        return `${tripRaw.value.start_date ?? "..."} - ${tripRaw.value.end_date ?? "..."}`;
      }
      return "...";
    });
  
    const budget = computed(() => {
      return `${tripRaw.value?.budget?.amount ?? "..."}`;
    });
  
    const participantCount = computed(() => {
      return `${tripRaw.value?.members?.length ?? 0} Uczestników`;
    });
  
    const activityCount = computed(() => "0 Aktywności");
  
    const upcomingActivities = computed(() => []);
  
    const tripName = computed(() => {
      return tripRaw.value?.name ?? "...";
    });
  
    const members = computed(() => {
      return tripRaw.value?.members ?? [];
    });
  
    const boxes = computed(() => [
      {
        title: "Czas trwania",
        icon: "mdi-calendar-month-outline",
        content: tripTime.value,
        set: {
          order: 1,
          size: {
            xs: { col: 12, row: 1 },
            sm: { col: 12, row: 1 },
            md: { col: 6, row: 1 },
            lg: { col: 3, row: 1 },
          },
        },
      },
      {
        title: "Budżet",
        icon: "mdi-currency-usd",
        content: {
          expenses: 200,
          amount: Number(budget.value),
          currency: "PLN",
          convertedAmount: Number(budget.value) * 0.24,
          convertedCurrency: "EUR",
        },
        set: {
          order: 2,
          size: {
            xs: { col: 12, row: 1 },
            sm: { col: 12, row: 1 },
            md: { col: 6, row: 1 },
            lg: { col: 4, row: 1 },
          },
        },
      },
      {
        title: "Uczestnicy",
        icon: "mdi-account-multiple",
        content: participantCount.value,
        set: {
          order: 3,
          size: {
            xs: { col: 12, row: 1 },
            sm: { col: 12, row: 1 },
            md: { col: 6, row: 1 },
            lg: { col: 2, row: 1 },
          },
        },
      },
      {
        title: "Aktywności",
        icon: "mdi-clock-outline",
        content: activityCount.value,
        set: {
          order: 4,
          size: {
            xs: { col: 12, row: 1 },
            sm: { col: 12, row: 1 },
            md: { col: 6, row: 1 },
            lg: { col: 3, row: 1 },
          },
        },
      }
    ]);
  
    return { boxes, isLoading, error, tripName, members };
  };
  const removeParticipant = (idTrip: number, idParticipant: number) => 
    removeParticipantMutation.mutateAsync({ idTrip, idParticipant });
  const addParticipant = (idTrip: number,participant:{name:string, email:string}) =>
    addParticipantMutation.mutateAsync({ idTrip, participant });

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
    const btnPath = getRole() == Role.TURIST ? "tripDashboard" : "tripDashboardGuide";
    
    return {
      btn: [
        {
          title: "Zarządzaj wycieczką",
          class: ["primary"],
          onclick: (id: string) =>
            router.push({ name: btnPath, params: { tripId: id } }),
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
          onclick: (trip: string, id: string) =>
              router.push({ name: "ActivityView", params: { tripId: trip, planId: id } }),
        },
        {
          title: "usuń plan",
          class: ["accent"],
          onclick: (tripId: string,itineraryId:string) => handleDeleteItinerary(tripId,itineraryId),
        },
      ],
      plans: getPlans,
    };
  });
  const tripMutationBudget = useMutation({
    mutationFn: saveBudget,
    onSuccess: () => {
      setSuccessCurrentMessage("zapisano");
      router.push({ name: "tripDashboard" });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message ||"błąd");
    },
  });
  const removeParticipantMutation = useMutation({
    mutationFn: ({ idTrip, idParticipant }: { idTrip: number, idParticipant: number }) => fetchRemoveParticipant( idTrip, idParticipant ),
    onSuccess: (idTrip) => {
      setSuccessCurrentMessage("Poprawnie usunięto uczestnika");
      queryClient.invalidateQueries({ queryKey: ["trip", String(idTrip)] });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message ||"błąd");
    },
  });
  const addParticipantMutation = useMutation({
    mutationFn: ({ idTrip, participant }: { idTrip: number, participant: {name:string, email:string} }) => fetchAddParticipant( idTrip, participant ),
    onSuccess: (idTrip) => {
      setSuccessCurrentMessage("poprawnie dodano uczestnika");
      console.log("idTrip", idTrip);
      queryClient.invalidateQueries({ queryKey: ["trip", String(idTrip)] });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message ||"błąd");
    },
  });
  const planMutationAdd = useMutation({
    mutationFn: ({ data, tripId }: { data: Plan; tripId: number }) =>
      createPlan(data, { tripId: String(tripId) }),
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

  const tripMutationUpdate = useMutation({
    mutationFn: ({ tripId, newData }: { tripId: string; newData: Partial<Trip> }) => {
      return updateTrip({ tripId }, newData);
    },
    onSuccess: () => {
      setSuccessCurrentMessage("Zaktualizowano wycieczkę");
    },
    onError: (err: any) => {
      setErrorCurrentMessage(err?.message || "Błąd podczas aktualizacji wycieczki");
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
    tripMutationUpdate,
    removeParticipant,
    addParticipant
  };
});
