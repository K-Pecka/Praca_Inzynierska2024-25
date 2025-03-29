import { defineStore } from "pinia";
import { ref } from "vue";
import { useNotificationStore } from "@/stores";
import { NewTrip } from "@/type";
export const useMockupStore = defineStore(
  "mockup",
  () => {
    const profile = {
      admin: 0,
      tourist: 1,
      touristPremium: 2,
      guide: 3,
    }
    const guide = {
      id: 1,
      email: "qwerty@wp.pl",
      first_name: "guide",
      last_name: "Kowalski",
      date_of_birth: "2001-01-01",
      password: "123",
      profile: [1, 2],
    };
    const tourist = {
      id: 1,
      email: "123@wp.pl",
      first_name: "Tourist",
      last_name: "Kowalski",
      date_of_birth: "2001-01-01",
      password: "123",
      profile: [1, 2],
    };
    const currentUser = ref<number>(tourist.id);
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
    const plan = {
      id: 1,
      name: "Test 1 - plan 1",
      country: "test",
      start_date: "2025-03-28",
      end_date: "2025-03-28",
      trip: 2
    }
    const data = ref({
      user: [tourist, guide],
      trip: [trip, trip2],
      plan: [plan,{...plan, id: 2}],
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
      console.log(id);
      return data.value.trip.find((t) => t.id == id);
    }
    const setBudget = (newBudget: any, id: number) => {
      const trip = data.value.trip.find((t) => t.id == id);
      console.log(trip);
      if (trip == undefined) {return null}
      trip.budget = newBudget;
      return {};
    }
    const getPlans = (id: number) => {
      const plans = data.value.plan.filter((p) => p.trip == id);
      console.log(plans);
      return plans == undefined || plans.length==0 ? null : plans;
    }
    const deletePlanMockUp = (id: number) => {
      console.log(id);
      data.value.plan = data.value.plan.filter((p) => p.id !== id);
      console.log(data.value.plan);
      return {};
    };
    const createPlanMockUp = (newPlan: any, param: Record<string, string> = {}) => {
      const trip = data.value.trip.find((t) => t.id == Number(param.tripId));
      if (trip == undefined) {
        return null;
      }
      let idPlan = data.value.plan[data.value.plan.length - 1].id;
      let newData = { 
        id: idPlan + 1,
        name: newPlan.name,
        country: newPlan.country,
        start_date: newPlan.start_date,
        end_date: newPlan.end_date,
        trip: Number(param.tripId),
      };
      data.value.plan.push(newData);
      console.log(data.value.plan);
      return newData;
    };
    const getUserProfile = () =>{
      const auth = localStorage.getItem("auth");
      if (auth) {
        currentUser.value = JSON.parse(auth).token.access;
      } else {
        currentUser.value = data.value.user[0].id;
      }
      const profile = data.value.user.find((t) => t.id == currentUser.value)?.profile
      return profile? profile: [];
    }
    return {getUserProfile, login, logOut, getTrips,getTrip, deleteTrip, addTrip,setBudget,getPlans, deletePlanMockUp,createPlanMockUp };
  },
  {
    persist: {
      storage: localStorage,
      pick: ["currentUser", "data"],
    },
  }
);
