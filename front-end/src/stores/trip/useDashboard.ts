import {computed} from "vue";
import {useQuery} from "@tanstack/vue-query";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {fetchTrip} from "@/api";
import {Role} from "@/type/enum";
import type {Trip} from "@/type";

function formatPL(dateString: string) {
    const dateObj = new Date(dateString);
    if (isNaN(dateObj.getTime())) return dateString;
    return new Intl.DateTimeFormat("pl-PL").format(dateObj);
}

export const useDashboard = () => {
    const {getRole} = useRoleStore();

    const getExpenseItem = () => {
        return {
            expenseItem: [
                {
                    title: "test",
                    date: "12-02-2022",
                    type: "food",
                    note: "bla bla bla",
                    amount: 100,
                    currency: "PLN",
                },
                {
                    title: "test",
                    date: "12-02-2022",
                    type: "food",
                    note: "bla bla bla",
                    amount: 100,
                    currency: "PLN",
                },
            ],
            sectionName:
                getRole() == Role.TURIST
                    ? "Twoje ostatnie wydatki"
                    : "Ostatnie zaległości uczestników",
        };
    };

    const getTripDetails = (id: number) => {
        return useQuery<Trip, Error, Trip, [string, number]>({
            queryKey: ["trip", id],
            queryFn: fetchTrip,
            //keepPreviousData: true,
        });
    };

    const getDashboard = (id: string) => {
        const {data: tripRaw, isLoading, error} = getTripDetails(Number(id));

        const tripTime = computed(() => {
            if (!tripRaw.value) return "...";
            return `${formatPL(tripRaw.value.start_date)} - ${formatPL(
                tripRaw.value.end_date
            )}`;
        });

        const budget = computed(() => `${tripRaw.value?.budget?.amount ?? "..."}`);
        const participantCount = computed(
            () => `${tripRaw.value?.members?.length ?? 0} Uczestników`
        );

        const activityCount = computed(() => ({
            icon: getRole() == Role.TURIST ? "mdi-clock-outline" : "mdi-email",
            title: getRole() == Role.TURIST ? "Aktywności" : "Wiadomości",
            content: getRole() == Role.TURIST ? "0 Aktywności" : "0 Wiadomości",
        }));

        const tripName = computed(() => tripRaw.value?.name ?? "...");
        const members = computed(() => tripRaw.value?.members ?? []);

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
                    expenses: 200,
                    amount: Number(budget.value),
                    currency: "PLN",
                    convertedAmount: Number(budget.value) * 0.24,
                    convertedCurrency: "EUR",
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

        return {boxes, isLoading, error, tripName, members};
    };

    return {getDashboard, getTripDetails, getExpenseItem};
};
