import {computed, ref} from "vue";
import {useRoleStore} from "@/stores/auth/useRoleStore";
import {Role} from "@/types/enum";

import {sectionDashboard} from "@/data/section/sectionName";
import {useBudget} from "./useBudget";
import {useTrips} from "./useTrips";
import { useDebt } from "./useDebt";
import { useAuthStore } from "../auth/useAuthStore";

function formatPL(dateString: string) {
    const dateObj = new Date(dateString);
    if (isNaN(dateObj.getTime())) return dateString;
    return new Intl.DateTimeFormat("pl-PL").format(dateObj);
}

export const useDashboard = (tripId: Function) => {
    const {getRole} = useRoleStore();
    const {getExpenseByTrip} = useBudget(tripId);
    const {getTripDetails} = useTrips(tripId);
    const {getDebt} = useDebt(tripId);
    const {userData} = useAuthStore();
    const {getActiveProfile} = userData;
    const getSpecialSectionName = ref(null);
    const getDashboard = () => {
        const {trip, isLoading_trip, error_trip} = getTripDetails(tripId());
        const {debt} = getDebt();
        const {expensesByTrip,isLoading_expenses} = getExpenseByTrip();
        const getSpecialSectionName = () => sectionDashboard(Number(trip?.value?.creator?.type) === 2? Role.GUIDE: Role.TOURIST,getActiveProfile()?.type == 2);
        const tripTime = computed(() => {
            if (!trip.value) return "...";
            return `${formatPL(trip.value.start_date)} - ${formatPL(
                trip.value.end_date
            )}`;
        });
        const typeGuide=computed(()=>Number(trip?.value?.creator?.type) === 2)
        const debtAmount = computed(() => {

        if (Array.isArray(debt.value) && getActiveProfile()?.type != 2) {
            return debt.value.reduce((acc, item) => {
            const amount = item.members.find(el=>el.id == getActiveProfile()?.id) ? parseFloat(item.amount_per_member_in_pln):0;
            return acc + (isNaN(amount) ? 0 : amount);
            }, 0);
        }
        else
        {
            return debt?.value?.reduce((acc, item) => {
            const amount = parseFloat(item.amount_in_pln);
            return acc + (isNaN(amount) ? 0 : amount);
            }, 0);
        }
        });
        const budget = computed(() => `${trip.value?.budget_amount ?? "..."}`);
        const members = computed(() => [...trip.value?.members ?? [], ...trip.value?.pending_members ?? []]);
        const participantCount = computed(
            () => `${members.value.length ?? 0} ${members.value.length == 1 ? "Uczestnik" : "Uczestników"}`
        );

        const activityCount = computed(() => ({
            icon:  "mdi-clock-outline",
            title: "Aktywności",
            content: Number(trip?.value?.creator?.type) !== 2
                ? [`${trip.value?.activity_count ?? 0} Aktywności`]
                : [`dziś: ${trip.value?.activity_for_today}`,` w tym tygodniu: ${trip.value?.activity_for_week}`],
        }));

        const tripName = computed(() => trip.value?.name ?? "...");
        const budgetBox = computed(()=>{
            if ( Number(trip?.value?.creator?.type) === 2 )
            {
                return {
                    title: "Długi",
                    icon: "mdi-currency-usd",
                    content: [`${debtAmount.value} PLN`],
                    set: {
                        order: 2,
                        size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}}
                    },
                }
            }
            else{
                return {
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
                }
            }
        })
        const expenses = computed(() => expensesByTrip.value?.reduce((acc, expense) => Number(acc) + Number(expense.converted_amount), 0) ?? 0);
        const boxes = computed(() => [
            {
                title: "Czas trwania",
                icon: "mdi-calendar-month-outline",
                content: [tripTime.value],
                className: ["font-weight-bold"],
                set: {
                    order: 1,
                    size: {xs: {col: 12, row: 1}, sm: {col: 12, row: 1}, md: {col: 6, row: 1}, lg: {col: 3, row: 1}},
                },
            },
            budgetBox.value,
            {
                title: "Uczestnicy",
                icon: "mdi-account-multiple",
                content: [participantCount.value],
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

        return {boxes, isLoading_trip, error_trip, tripName,debt,typeGuide,getSpecialSectionName,expensesByTrip,isLoading_expenses};
    };

    return {getDashboard, getSpecialSectionName};
};