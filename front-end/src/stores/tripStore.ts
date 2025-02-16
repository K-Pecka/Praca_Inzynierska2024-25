import { useMutation, useQuery, useQueryClient, UseQueryOptions } from "@tanstack/vue-query";
import { defineStore } from "pinia";
import { computed } from "vue";
import { useUserStore } from "./userStore";
import router from "@/router";
import { useMessageStore } from "./messageStore";
interface Button {
  title: string;
  class: String[];
  onclick: (id: number | undefined) => void;
}
export const useTripStore = defineStore("trip", () => {
  const queryClient = useQueryClient();

  const { setErrorCurrentMessage, setSuccessCurrentMessage } =
    useMessageStore();
  const { getToken } = useUserStore();

  const fetchTrips = async () => {
    const response = await fetch("https://api.plannder.com/trip/all/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
    });

    if (!response.ok) {
      throw new Error("Błąd podczas pobierania wycieczek");
    }

    return response.json();
  };
  const fetchPlans = async (id:Number) => {
    console.log(id);
    const response = await fetch(`https://api.plannder.com/trip/${id}/itinerary/all/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
    });

    if (!response.ok) {
      throw new Error("Błąd podczas pobierania wycieczek");
    }

    return response.json();
  };
  const fetchTripDetails = async (id: Number) => {
    const response = await fetch(`https://api.plannder.com/trip/${id}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
    });

    if (!response.ok) {
      throw new Error("Błąd podczas pobierania wycieczek");
    }

    return response.json();
  };
  const deleteTrip = async (tripId: Number) => {
    const response = await fetch(`https://api.plannder.com/trip/${tripId}/delete/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
    });
  
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData);
    }
    return response;
  };
  const deleteTripMutation = useMutation({
    mutationFn: deleteTrip,
    onSuccess: () => {
      setSuccessCurrentMessage("Pomyślnie usunięto wycieczkę");
      queryClient.invalidateQueries({ queryKey: ["trips"] });
    },
    onError: (err) => {
      setErrorCurrentMessage(err.message);
    }    
  });
  const handleDeleteTrip = async (id: Number) => {
    try {
      await deleteTripMutation.mutateAsync(id);
    } catch (err) {
      console.error("Failed to delete trip:", err);
    }
  };
  
  const getTripDetails = (id: number) => {
    return useQuery({
      queryKey: ["trip", id],
      queryFn: () => fetchTripDetails(id),
    });
  };
  const getPlans = (id: number) => {
    return useQuery({
      queryKey: ["plans", id],
      queryFn: () => fetchPlans(id),
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
          onclick: (id: Number) => router.push(`/panel/YourTrip/${id}`),
        },
        {
          title: "usuń wycieczkę",
          class: ["accent"],
          onclick: (id: number) => handleDeleteTrip(id),
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
          onclick: (id: Number) => router.push(`/panel/YourTrip/${id}`),
        },
        {
          title: "usuń wycieczkę",
          class: ["accent"],
          onclick: (id: number) => handleDeleteTrip(id),
        },
      ],
      plans: getPlans,
    };
  });
  const saveBudget = async (data: {
    amount: string;
    currency: string;
    trip: Number;
  }) => {
    const response = await fetch(`https://api.plannder.com/trip/${data.trip}/budget/update/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
      body: JSON.stringify(data),
    });
    console.log(data);
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData || "unknow");
    }

    return response.json();
  };
  const tripMutationBudget = useMutation({
    mutationFn: saveBudget,
    onSuccess: (data) => {
      setSuccessCurrentMessage("zapisano");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  const addTrip = async (data: {
    name: string;
    start_date: Date;
    end_date: Date;
  }) => {
    const response = await fetch(`https://api.plannder.com/trip/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
      body: JSON.stringify(data),
    });
    console.log(data);
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData || "unknow");
    }

    return response.json();
  };
  const addPlan = async ({
    data,
    tripId
  }: {
    data: {
      name: string;
      start_date: Date;
      end_date: Date;
    };
    tripId: number;
  })  => {
    console.log( data,
      tripId);
    const response = await fetch(`https://api.plannder.com/trip/${tripId}/itinerary/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
      body: JSON.stringify(data),
    });
    console.log(data);
    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData);
      throw new Error(errorData || "unknow");
    }

    return response.json();
  };
  const planMutationAdd = useMutation({
    mutationFn: addPlan,
    onSuccess: (data) => {
      router.back();
      setSuccessCurrentMessage("dodano planu");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  const tripMutationAdd = useMutation({
    mutationFn: addTrip,
    onSuccess: (data) => {
      router.back();
      setSuccessCurrentMessage("dodano wycieczkę");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  return { yourTrips,yourPlans, getTripDetails,tripMutationAdd, tripMutationBudget,planMutationAdd };
});
