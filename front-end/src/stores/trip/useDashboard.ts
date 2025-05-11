import {computed} from "vue";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {Role} from "@/types/enum";

import {sectionDashboard} from "@/data/section/sectionName";
import {useBudget} from "./useBudget";
import {useTrips} from "./useTrips";

function formatPL(dateString: string) {
    const dateObj = new Date(dateString);
    if (isNaN(dateObj.getTime())) return dateString;
    return new Intl.DateTimeFormat("pl-PL").format(dateObj);
}

export const useDashboard = (tripId: Function) => {
    const {getRole} = useRoleStore();
    const {getExpenseByTrip} = useBudget(tripId);
    const {getTripDetails} = useTrips(tripId);

    const getSpecialSectionName = () => sectionDashboard(getRole());

    // DO POPRAWY TEN SEGEMENT
    const getDashboard = () => {

        const {trip, isLoading_trip, error_trip} = getTripDetails(tripId());
        const {expensesByTrip} = getExpenseByTrip(tripId());
        const tripTime = computed(() => {
            if (!trip.value) return "...";
            return `${formatPL(trip.value.start_date)} - ${formatPL(
                trip.value.end_date
            )}`;
        });
        const budget = computed(() => `${trip.value?.budget_amount ?? "..."}`);
        const members = computed(() => [...trip.value?.members ?? [], ...trip.value?.pending_members ?? []]);
        const participantCount = computed(
            () => `${members.value.length ?? 0} ${members.value.length == 1 ? "Uczestnik" : "Uczestników"}`
        );

        const activityCount = computed(() => ({
            icon: getRole() == Role.TURIST ? "mdi-clock-outline" : "mdi-email",
            title: getRole() == Role.TURIST ? "Aktywności" : "Wiadomości",
            content: getRole() === Role.TURIST
                ? `${trip.value?.activity_count ?? 0} Aktywności`
                : "Wiadomości",
        }));

        const tripName = computed(() => trip.value?.name ?? "...");

        const expenses = computed(() => expensesByTrip.value?.reduce((acc, expense) => Number(acc) + Number(expense.converted_amount), 0) ?? 0);
        const boxes = computed(() => [
            {
                title: "Czas trwania",
                icon: "mdi-calendar-month-outline",
                content: tripTime.value,
                className: ["font-weight-bold"],
                set: {
                    order: 1,
                    size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}},
                },
            },
            {
                title: "Budżet",
                icon: "mdi-currency-usd",
                content: {
                    expenses: expenses.value,
                    amount: Number(budget.value),
                    currency: "PLN"
                },
                set: {
                    order: 2,
                    size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}}
                },
            },
            {
                title: "Uczestnicy",
                icon: "mdi-account-multiple",
                content: participantCount.value,
                set: {
                    order: 3,
                    size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}}
                },
            },
            {
                title: activityCount.value.title,
                icon: activityCount.value.icon,
                content: activityCount.value.content,
                set: {
                    order: 4,
                    size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}}
                },
            },
        ]);

        return {boxes, isLoading_trip, error_trip, tripName, members};
    };

    return {getDashboard, getSpecialSectionName};
};