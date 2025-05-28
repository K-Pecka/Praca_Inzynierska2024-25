<script setup lang="ts">
import {
  DebtList,
  Section,
  HeaderSection,
  DebtForm,
  AppCard,
} from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { computed, ref } from "vue";
import { useMembersStore } from "@/stores/trip/useMembersStore";
import { useAuthStore } from "@/stores";
import { DebtDetails } from "@/types";

const toggleForm = () => {
  showForm.value = !showForm.value;
};
const { trip: tripStore,debt:debtStore } = useTripStore();
const { getTripDetails } = tripStore;
const { getDebt } = debtStore;
const {debt,isLoading_debt} = getDebt();
const { trip, isLoading_trip } = getTripDetails();

const members = computed(() => {
  if (trip.value !== undefined) {
    useMembersStore().setData(trip.value);
  }
  return useMembersStore().members.filter((e) => !e.is_guest && !e.is_owner) || [];
});


const onDebtAdded = () => {
  showForm.value = false;
};
const debtAmount = computed(() => {
  if (Array.isArray(debt.value) && getActiveProfile()?.type != 2) {
    return debt.value.reduce((acc, item) => {
      const amount = item.members.find(el=>el.id == getActiveProfile()?.id) ? parseFloat(item.amount_per_member):0;
      return acc + (isNaN(amount) ? 0 : amount);
    }, 0);
  }
  else
  {
    return debt?.value?.reduce((acc, item) => {
      const amount = parseFloat(item.amount);
      return acc + (isNaN(amount) ? 0 : amount);
    }, 0);
  }
});
const { userData } = useAuthStore();
const {getActiveProfile,isOwner} = userData;
const touristDebt = computed(() => {
  if (!Array.isArray(debt.value) || debt.value.length <= 0) {
    return null;
  }
  if (isOwner(trip.value?.creator.id || 0)) {
    return null;
  }
  return debt.value.filter((item) =>
    item.members.length > 0 &&
    item.members.some((member) => member.id === getActiveProfile()?.id)
  ) || null;
});
const showForm = ref(false);
const currency = "PLN"
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection
        subtitle="Zaległości"
        :button="getActiveProfile()?.type == 2"
        :button-text="(getActiveProfile()?.type != 2) ? '' : 'Dodaj'"
        :button-action="toggleForm"
      />
    </template>

    <template #content>
      <v-col cols="12" class="text-h5 font-weight-bold">
        <!-- Budget Overview -->
        <v-row class="budget-overview-gap">
          <!-- Budget Card -->
          <AppCard>
            <p class="mb-4 d-flex align-center" style="gap: 8px">
              Dług
            </p>
            <template v-if="isLoading_trip">
              <v-row justify="center">
                <v-col cols="auto">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="32"
                  />
                </v-col>
              </v-row>
            </template>
            <div v-else>
              <p class="text-h3 font-weight-bold mb-0" style="line-height: 1.2">
                {{ (debtAmount ?? 0).toFixed(2) }} {{ currency }}
              </p>
            </div>
          </AppCard>

          

          <!-- Form for adding expenses -->
          <v-col cols="12" v-if="showForm">
            <v-row>
              <DebtForm
                :isOwnerTrip="isOwner(trip?.creator?.id || 0)"
                :members="members"
                @cancelForm="showForm = false"
                @submitted="onDebtAdded"
                class="form-container"
              />
            </v-row>
          </v-col>

          <!-- List of expenses -->
          <v-col cols="12">
            <v-row>
              <AppCard cols="12">
                <!-- Header with title and filter button -->
                <v-row
                  justify="space-between"
                  align="center"
                  class="mb-4"
                  no-gutters
                >
                  <span>Istniejące długi</span>
                  
                </v-row>

                <!-- Expenses List -->
                <template v-if="!isLoading_debt">
                  <DebtList
                    :debts="touristDebt ?? (debt as DebtDetails[] | undefined)"
                    :currency="currency"
                    variant="manage"
                    :members="members"
                    :tripId="trip?.id"
                    :isOwnerTrip="isOwner(trip?.creator?.id || 0)"
                  />
                </template>
                <template v-else>
                  <v-row justify="center">
                    <v-col cols="auto">
                      <v-progress-circular
                        indeterminate
                        color="primary"
                        size="64"
                      />
                    </v-col>
                  </v-row>
                </template>
              </AppCard>
            </v-row>
          </v-col>
          
        </v-row>
      </v-col>

      
    </template>
  </Section>
</template>

<style scoped lang="scss">
.difference-positive {
  color: rgba(22, 163, 74, 0.75);
}
.difference-negative {
  color: rgb(var(--v-theme-delete));
}
</style>

