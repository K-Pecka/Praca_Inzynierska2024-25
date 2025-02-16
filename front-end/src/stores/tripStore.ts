import { useMutation, useQuery, UseQueryOptions } from "@tanstack/vue-query";
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
      throw new Error("błąd usuwania");
    }
    return response.json();
  };
  
  const deleteTripMutation = useMutation({
    mutationFn: deleteTrip,
    onSuccess: () => {
      setSuccessCurrentMessage("Pomyślnie usunięto wycieczkę");
    },
    onError: (err) => {
      console.table(err.message);
      if (err && typeof err === 'object' && err.message) {
        if (typeof err.message === 'object') {
          Object.entries(err.message).forEach(([key, value]) => {
            console.log(`${key}: ${value}`);
            setErrorCurrentMessage(`${value}`);
          });
        } else {
          setErrorCurrentMessage(err.message);
        }
      } else {
        setErrorCurrentMessage("An unexpected error occurred.");
      }
    }    
  });
  const handleDeleteTrip = async (id: Number) => {
    try {
      await deleteTripMutation.mutateAsync(id);
    } catch (err) {
      console.error("Failed to delete trip:", err);
    }
  };

  const getTrips = () => {
    return useQuery({
      queryKey: ["trips"],
      queryFn: fetchTrips,
    });
  };
  const getTripDetails = (id: number) => {
    return useQuery({
      queryKey: ["trip", id],
      queryFn: () => fetchTripDetails(id),
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
  const saveBudget = async (data: {
    amount: string;
    currency: string;
    trip: Number;
  }) => {
    const response = await fetch(`https://api.plannder.com/trip/${data.trip}/budget/`, {
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
  const tripMutationBudget = useMutation({
    mutationFn: saveBudget,
    onSuccess: (data) => {
      setSuccessCurrentMessage("zapisano");
    },
    onError: (err) => {
      setErrorCurrentMessage("błąd");
    },
  });
  return { yourTrips, getTripDetails, tripMutationBudget };
});
