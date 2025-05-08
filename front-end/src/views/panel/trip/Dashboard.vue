<script lang="ts" setup>
import {Box, Section, HeaderSection, ExpensesList} from "@/components";
<<<<<<< Updated upstream
import {useTripStore} from "@/stores/trip/useTripStore";

useTripStore().initialize();
const {dashboard, budget} = useTripStore();
const {getDashboard, getSpecialSectionName} = dashboard;
const {getExpensByTrip} = budget;

const {boxes, isLoading_trip, error_trip} = getDashboard();
const {expensesByTrip, isLoading_expenses} = getExpensByTrip();
=======
import {useTrip2Store} from "@/stores/trip/xd";
import {useRoute} from "vue-router";
import {watchEffect} from "vue";
import {useTripQuery} from "@/composables/useTrips";
import {useExpensesQuery} from "@/composables/useExpenses";
import AppCard from "@/components/AppCard.vue";

const route = useRoute();
const tripId = Number(route.params.tripId);
const {
  data: trip,
  isLoading: isLoading_trip,
  error: error_trip
} = useTripQuery(tripId);

const {
  data: expenses,
  isLoading: isLoading_expenses,
  error: error_expenses
} = useExpensesQuery(tripId);

const {sumExpensesToPLN} = useTrip2Store()
const store = useTrip2Store()

watchEffect(() => {
  if (trip?.value) {
    store.selectedTrip = trip.value
  }
  if (expenses?.value) {
    store.expenses = expenses.value
  }
})

>>>>>>> Stashed changes
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection subtitle="Panel"/>
    </template>
    <template #content>
<<<<<<< Updated upstream
      <!-- Loadder -->
      <template v-if="isLoading_trip"> Loading...</template>
      <template v-else-if="error_trip">Error ...</template>
      <template v-else>
        <v-col cols="12">
          <v-row class="budget-overview-gap">
            <v-col v-for="(box, index) in boxes" :key="index">
              <Box
                  :title="box.title"
                  :content="box.content"
                  :set="box.set"
                  :icon="box.icon"
                  class="color-text pb-5 h-100"
              />
            </v-col>
            <v-col cols="12">
              <v-card class="dashboard-card" elevation="4">
                <v-card-title
                    class="text-h5 pt-0 font-weight-bold expense-card-title"
                >
                  {{ getSpecialSectionName() }}
                </v-card-title>
                <!-- Loadder -->
                <template v-if="isLoading_expenses"> Loading expenses...</template>
                <ExpensesList
                    v-else
                    variant="view"
                    :limit="4"
                    :expenses="expensesByTrip"
                    no-icon
                />
=======

      <!-- Loader -->
      <v-row v-if="isLoading_trip"> Loading...</v-row>
      <v-row v-else-if="error_trip">Error ...</v-row>
      <v-row v-else class="w-100 text-h6 font-weight-bold budget-overview-gap">

        <!-- Dashboard -->
        <appCard cols="3">
          <p class="pb-4">
            <v-icon class="color-primary mr-3">mdi-calendar-month-outline</v-icon>
            <span>Czas trwania</span>
          </p>
          <p>
            <span class="text-h5 font-weight-bold">{{ trip?.start_date }} - {{ trip?.end_date }}</span>
          </p>
        </appCard>
        <appCard cols="3">
          <p class="pb-4">
            <v-icon class="color-primary mr-3">mdi-currency-usd</v-icon>
            <span>Budżet</span>
          </p>
          <p class="pb-2">
            <span class="text-h5 font-weight-bold"> {{ trip?.budget_amount }} PLN</span>
          </p>
          <p class="pb-2">
            <v-progress-linear
                :model-value="0.36 * 100"
                height="6"
                color="green"
                background-color="grey-lighten-3"
                rounded
            />
          </p>
          <p class="d-flex justify-space-between">
            <span style="color: rgba(22, 163, 74, .75)">{{ sumExpensesToPLN }} PLN</span>
            <span class="text-h6 font-weight-bold">
              {{
                trip?.budget_amount && Number(trip.budget_amount) !== 0 ? ((sumExpensesToPLN / Number(trip.budget_amount)) * 100).toFixed(2) : 0
              }}%
            </span>
          </p>
        </appCard>
        <appCard cols="3">
          <p class="pb-4">
            <v-icon class="color-primary mr-3">mdi-account-multiple</v-icon>
            <span>Uczestnicy</span>
          </p>
          <p>
            <span class="text-h5 font-weight-bold">{{ trip?.members?.length }} Uczestników</span>
          </p>
        </appCard>
        <appCard cols="3">
          <p class="pb-4">
            <v-icon class="color-primary mr-3">mdi-clock-outline</v-icon>
            <span>Aktywności</span>
          </p>
          <p>
            <span class="text-h5 font-weight-bold">{{ trip?.activity_count }} Aktywności</span>
          </p>
        </appCard>

        <!-- Trip overview -->
        <v-col cols="12">
          <v-row class="budget-overview-gap" no-gutters>
            <v-col v-for="(expense, index) in expenses" :key="index">

              <!-- Box -->
              <v-row
                  :title="expense.title"
                  class="h-100"
              />
            </v-col>

            <!-- Expenses card -->
            <v-col cols="12">
              <v-card class="background-secondary rounded-lg w-100 px-5 pb-3" elevation="4">
                <v-card-text>
                  <v-card-title
                      class="font-weight-bold text-h5 expense-card-title px-0 pb-4"
                  >
                    Twoje ostatnie wydatki
                  </v-card-title>

                  <!-- Loader -->
                  <template v-if="isLoading_expenses"> Loading expenses...</template>

                  <ExpensesList
                      v-else
                      variant="view"
                      :limit="4"
                      :expenses="expenses"
                  />
                </v-card-text>
>>>>>>> Stashed changes
              </v-card>
            </v-col>
          </v-row>
        </v-col>
<<<<<<< Updated upstream
      </template>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  font-size: 2rem;
}

h1 {
  text-align: start;
  font-size: 2rem;
}

.dashboard-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  border-radius: 12px;
  padding: 1.5rem;
}

.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>
=======
      </v-row>
    </template>
  </Section>
</template>
>>>>>>> Stashed changes
