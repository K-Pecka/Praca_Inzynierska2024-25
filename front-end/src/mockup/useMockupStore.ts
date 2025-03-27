import { defineStore } from "pinia";
import { ref } from "vue";
import { useNotificationStore } from "@/stores";
import { NewTrip } from "@/type";
export const useMockupStore = defineStore(
  "mockup",
  () => {
    const user = {
      id: 1,
      email: "qwerty@wp.pl",
      first_name: "Jan",
      last_name: "Kowalski",
      date_of_birth: "2001-01-01",
      password: "123",
      profile: [1, 2],
    };
    const currentUser = ref<number>(user.id);
    const trip = {
      id: 2,
      name: "Test 1",
      creator: 1,
      country: "Polska",
      city: "Warszawa",
      members: [],
      budget: {
        id: 2,
        amount: "0.00",
        currency: "PLN",
        trip: 2,
      },
      start_date: "2025-04-16",
      end_date: "2025-04-26",
    };
    const trip2 = {
      id: 3,
      name: "Test 2",
      creator: 1,
      members: [],
      budget: {
        amount: "0.00",
        currency: "PLN",
        trip: 2,
      },
      start_date: "2025-04-16",
      end_date: "2025-04-26",
    };
    const data = ref({
      user: [user],
      trip: [trip, trip2],
      plan: [],
      ticket: [],
      budget: [],
    });

    const login = (email: string, password: string) => {
      const foundUser = data.value.user.find(
        (u) => u.email === email && u.password === password
      );
      console.log(foundUser);
      if (foundUser) {
        currentUser.value = foundUser.id;
        return { access: foundUser.id, refresh: "refresh" };
      } else {
        const { loginError } = useNotificationStore();
        throw new Error(loginError());
      }
    };
    const logOut = () => {
      localStorage.removeItem("auth");
    };

    const getTrips = () => {
      const auth = localStorage.getItem("auth");
      console.log(auth);
      if (auth) {
        currentUser.value = JSON.parse(auth).token.access;
      } else {
        currentUser.value = data.value.user[0].id;
        return [];
      }
      const trips = data.value.trip.filter(
        (t) => t.creator == Number(currentUser.value)
      );
      return trips == undefined ? null : trips;
    };

    const deleteTrip = (id: number) => {
      data.value.trip = data.value.trip.filter((t) => t.id !== id);
    };
    const addTrip = (newTrip: NewTrip) => {
      const auth = localStorage.getItem("auth");
      if (auth) {
        currentUser.value = JSON.parse(auth).token.access;
      } else {
        currentUser.value = data.value.user[0].id;
      }
      let idTrip = data.value.trip[data.value.trip.length - 1].id;
      let newData = {
        id: idTrip + 1,
        name: newTrip.name,
        creator: currentUser.value,
        members: [],
        budget: {
          amount: "0.00",
          currency: "PLN",
          trip: idTrip + 1,
        },
        start_date: newTrip.start_date,
        end_date: newTrip.end_date,
      };
      data.value.trip.push(newData);
    };
    const getTrip = (id: number) => {
      return data.value.trip.find((t) => t.id == id);
    }
    return { login, logOut, getTrips,getTrip, deleteTrip, addTrip };
  },
  {
    persist: {
      storage: localStorage,
      pick: ["currentUser", "data"],
    },
  }
);
