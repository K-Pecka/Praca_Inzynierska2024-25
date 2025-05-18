<script setup lang="ts">
import { Expense } from "@/types";
import AppCard from "@/components/AppCard.vue";
import { useAuthStore, useUtilsStore } from "@/stores";
import { AppButton } from "@/components";
import { useTripStore } from "@/stores";

const { budget } = useTripStore();
const { deleteExpense } = budget;

const { mapCategoryBudget } = useUtilsStore();
const { expense, isOwnerTrip } = defineProps<{
  isOwnerTrip: boolean;
  expense: Expense;
  variant?: "manage" | "view";
  noIcon?: boolean;
}>();

const { icon, name: categoryName } = mapCategoryBudget(expense.category);
const currencyValue =
  expense.currency != "PLN" ? `(${expense.converted_amount} PLN)` : "";
const { getUser } = useAuthStore();
const hasPermissionToDelete = (userId: number) => {
  return isOwnerTrip || getUser()?.profiles?.some(p => p.id === userId);
};
</script>

<template>
  <AppCard
    class="background-card"
    no-padding
    bg-transparent
    :elevation="0"
    cols="12"
  >
    <v-card-text class="text-h6 font-weight-bold">
      <v-row justify="space-between" align="center">
        <!-- Expense Icon and Title -->
        <v-col>
          <v-row align="center">
            <v-sheet class="rounded-xl bg-red mr-4">
              <v-icon size="24" class="ma-1">
                {{ icon }}
              </v-icon>
            </v-sheet>
            <v-row class="flex-column" justify="center" no-gutters>
              <span>{{ expense.title }}</span>
              <span class="text-subtitle-1 font-weight-medium">
                <span> {{ expense.date }} </span>
                <span class="px-3"> {{ expense.username }}</span>
                <span class="notes"> {{ expense?.note ?? "" }}</span>
                <span class="category">{{ categoryName }}</span>
              </span>
            </v-row>
          </v-row>
        </v-col>

        <!-- Expense Amount -->
        <v-col class="text-h5 text-end" cols="12" sm="5" md="5" lg="5">
          <v-row
            :class="
              variant === 'manage' ? 'justify-space-between' : 'justify-end'
            "
            no-gutters
          >
            <v-col cols="auto" sm="12" md="6" lg="8" class="pb-2">
              <v-row class="flex-column justify-center" no-gutters>
                <strong class="text-black-70 mr-2">
                  {{ expense.amount }} {{ expense.currency }}
                </strong>
                <span
                  v-if="currencyValue"
                  class="text-subtitle-1 text-grey-darken-1"
                  style="line-height: 0.8"
                >
                  {{ currencyValue }}
                </span>
                <span v-else class="text-subtitle-1" style="line-height: 0.8">
                  ({{ expense.amount }} {{ expense.currency }})
                </span>
              </v-row>
            </v-col>
            <template v-if="expense && expense.trip && variant == 'manage'">
              <v-col cols="auto" sm="12" md="6" lg="4"
                ><AppButton
                  color="red"
                  font-auto
                  max-width="190px"
                  text="Usuń Wydatek"
                  @click="
                    hasPermissionToDelete(expense.user)
                      ? deleteExpense.mutate({
                          expenseId: String(expense.id),
                          tripId: String(expense.trip),
                        })
                      : () => {}
                  "
                  :disabled="!hasPermissionToDelete(expense.user)"
                />
              </v-col>
            </template>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </AppCard>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.category {
  color: rgb($primary-color);
  font-weight: 400;
}

.notes {
  color: #757575;
}

.amount {
  color: #e74c3c;
}

.background-card {
  background-color: rgb(var(--v-theme-background));
}
</style>
