import {defineStore} from "pinia";
import {ref} from "vue";
import {useNotificationStore} from "@/stores";
import {NewTrip} from "@/types";

interface Participant {
    id: number;
    name: string;
    email: string;
}

interface Budget {
    id: number,
    amount: string;
    currency: string;
    trip: number;
}

interface Trip {
    id: number;
    name: string;
    creator: number;
    country?: string;
    city?: string;
    members: Participant[];
    budget: Budget;
    start_date: string;
    end_date: string;
}

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
            id: 2,
            email: "123@wp.pl",
            first_name: "Tourist",
            last_name: "Kowalski",
            date_of_birth: "2001-01-01",
            password: "123",
            profile: [1],
        };
        const currentUser = ref<number>(tourist.id);
        const trip: Trip = {
            id: 2,
            name: "Test 1",
            creator: 1,
            country: "Polska",
            city: "Warszawa",
            members: [{
                id: 1, name: "string 1", email: "string"
            }, {
                id: 2, name: "string 2", email: "string"
            }, {
                id: 3, name: "string 3", email: "string"
            },],
            budget: {
                id: 2,
                amount: "0.00",
                currency: "PLN",
                trip: 2,
            },
            start_date: "2025-04-16",
            end_date: "2025-04-26",
        };
        const trip2: Trip = {
            id: 3,
            name: "Test 2",
            creator: 1,
            members: [],
            budget: {
                id: 3,
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
            trip: [trip, trip2, {...trip2, id: 3, creator: 2}],
            plan: [plan, {...plan, id: 2}],
            ticket: [],
            budget: [],
        });

        const login = (email: string, password: string) => {
            const foundUser = data.value.user.find(
                (u) => u.email === email && u.password === password
            );
            if (foundUser) {
                currentUser.value = foundUser.id;
                return {access: foundUser.id, refresh: "refresh"};
            } else {
                const {loginError} = useNotificationStore();
                throw new Error(loginError());
            }
        };
        const logOut = () => {
            localStorage.removeItem("auth");
        };

        const getTrips = () => {
            const auth = localStorage.getItem("auth");
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
            if (auth != null) {
                currentUser.value = JSON.parse(auth).token.access;
            } else {
                currentUser.value = data.value.user[0].id;
            }
            let idTrip = data.value.trip[data.value.trip.length - 1].id;
            let newData: Trip = {
                id: idTrip + 1,
                name: newTrip.name,
                creator: currentUser.value,
                members: [],
                budget: {
                    id: new Date().getMilliseconds(),
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
        const setBudget = (newBudget: any, id: number) => {
            const trip = data.value.trip.find((t) => t.id == id);
            if (trip == undefined) {
                return null
            }
            trip.budget = newBudget;
            return {};
        }
        const getPlans = (id: number) => {
            const plans = data.value.plan.filter((p) => p.trip == id);
            return plans == undefined || plans.length == 0 ? null : plans;
        }
        const deletePlanMockUp = (id: number) => {
            data.value.plan = data.value.plan.filter((p) => p.id !== id);
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
            return newData;
        };
        const getUserProfile = () => {
            const auth = localStorage.getItem("auth");
            if (auth != null && JSON.parse(auth)?.token) {
                currentUser.value = JSON.parse(auth).token.access;
            } else {
                currentUser.value = 0;
            }
            const profile = data.value.user.find((t) => t.id == currentUser.value)?.profile
            return profile ? profile : [];
        }
        const addParticipant = (idTrip: number, participant: { name: string; email: string }) => {
            const trip = data.value.trip.find((t) => t.id === idTrip);
            if (!trip) return {error: true, message: "Podana wycieczka nie istnieje"};

            const isAlreadyMember = trip.members.some((m: { email: string }) => m.email === participant.email);
            if (isAlreadyMember) return {error: true, message: "Dodano już takiego użytkownika"};

            const newId = trip.members.length > 0 ? Math.max(...trip.members.map((m: { id: number }) => m.id)) + 1 : 1;
            const newParticipant = {id: newId, ...participant};

            trip.members.push(newParticipant);
        };
        const removeParticipant = (idTrip: number, idParticipant: number) => {
            const trip = data.value.trip.find((t) => t.id === idTrip);

            if (trip) {
                trip.members = trip.members.filter((member) => member.id !== idParticipant);
                return;
            }
            return {error: true, message: "Podana wycieczka nie działa"}
        };

        const getCurrentUser = () => {
            return data.value.user.find((u) => u.id === currentUser.value);
        };

        const getUserInitials = () => {
            const user = getCurrentUser();
            if (!user) return "";
            const initials = `${user.first_name[0] ?? ""}${user.last_name[0] ?? ""}`;
            return initials.toUpperCase();
        };

        const updateProfileMockUp = (
            payload: {
                first_name?: string; last_name?: string;
                current_password?: string; new_password?: string
            }
        ) => {
            const user = data.value.user.find(u => u.id === currentUser.value);
            if (!user) return {error: true, message: 'Brak użytkownika'};

            if (payload.new_password) {
                if (user.password !== payload.current_password)
                    return {error: true, message: 'Błędne aktualne hasło'};
                user.password = payload.new_password;
            }

            if (payload.first_name) user.first_name = payload.first_name;
            if (payload.last_name) user.last_name = payload.last_name;

            return {first_name: user.first_name, last_name: user.last_name};
        }

        return {
            removeParticipant,
            addParticipant,
            getUserProfile,
            login,
            logOut,
            getTrips,
            getTrip,
            deleteTrip,
            addTrip,
            setBudget,
            getPlans,
            deletePlanMockUp,
            createPlanMockUp,
            getUserInitials,
            updateProfileMockUp
        };
    },
    {
        persist: {
            storage: localStorage,
            pick: ["currentUser", "data"],
        },
    }
);
