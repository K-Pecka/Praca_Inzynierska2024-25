<script lang="ts" setup>
import { Box, Section, HeaderSection, ExpensesList } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import AppLoader from "@/components/shared/AppLoader.vue";
import { onMounted } from "vue";
import { DebtList} from "@/components";
import { DebtDetails } from "@/types";
const tripStore = useTripStore();

const {
  boxes,
  isLoading_trip,
  error_trip,
  getSpecialSectionName,
  expensesByTrip,
  isLoading_expenses,
  debt,
  typeGuide
} = tripStore.dashboard.getDashboard();

onMounted(() => {
  useTripStore().initialize();
});
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection subtitle="Panel" />
    </template>
    <template #content>
      <!-- Loadder -->
      <template v-if="isLoading_trip">
        <AppLoader text="Ładowanie danych..." />
      </template>
      <template v-else-if="error_trip">Error ...</template>
      <template v-else>
        <v-col cols="12">
          <v-row class="budget-overview-gap">
            <v-col v-for="box in boxes" :key="box.title">
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
                <template v-if="isLoading_expenses">
                  Loading expenses...</template
                >
                <DebtList v-if="typeGuide"
                    :debts="debt ?? (debt as DebtDetails[] | undefined)"
                    :limit=4
                  />
                <ExpensesList
                  v-else
                  variant="view"
                  :limit="4"
                  :expenses="expensesByTrip"
                  no-icon
                />
                
              </v-card>
            </v-col>
          </v-row>
        </v-col>
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
