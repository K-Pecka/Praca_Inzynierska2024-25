import { defineStore } from "pinia";
import { computed } from "vue";

export const useTripStore = defineStore("trip", () => {
  const deleteTrip = (id: number) => {
    alert(`usuń id:${id}`)
  };
  const getAllTrip = () =>{
    
  }
  const yourTrips = computed(() => {
    return {
      btn: [
        {
          title: "Zarządzaj wycieczką",
          class:['primary'],
          onclick: (id: Number) => alert("wycieczka"),
        },
        {
          title: "Zarządzaj wycieczką",
          class:['accent'],
          onclick: (id: number) => deleteTrip(id),
        },
      ],
      trip: [
        {
          id: 1,
          title: "Majówka w Paryżu",
          date: "01.03.2025 - 04.03.2025",
          image: "/picture/p1.svg"
        },
        {
            id: 2,
            title: "Majówka w Paryżu",
            date: "01.03.2025 - 04.03.2025",
            image: "/picture/p1.svg"
          },
      ],
    };
  });

  return { yourTrips };
});
