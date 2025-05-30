<script setup lang="ts">
import { ref } from "vue";
import AppCard from "@/components/AppCard.vue";
import { useTripStore,useAuthStore } from "@/stores";
import {DebtDetails } from "@/types"
const {userData} = useAuthStore();
const {getActiveProfile} = userData;

const props = defineProps<{
  debt: DebtDetails;
}>();

const dialog = ref(false);
import { useUtilsStore } from "@/stores";

const { getTripId } = useUtilsStore();
const {debt} = useTripStore();
const { removeMember,deleteDebt } = debt;

const markAsPaid = (profile: number) => { 
  removeMember.mutate(
    {
      profileId: String(profile),
      debtId: String(props.debt.id),
      tripId: String(getTripId())
    },
    {
      onSuccess: () => {
        if (props.debt.members.length == 1) {
          deleteDebt.mutate(
            {
              tripId: String(getTripId()),
              debtId: String(props.debt.id)
            },
            {
              onSuccess: () => {
                dialog.value = false;
              }
            }
          );
        }
      }
    }
  );
};
const openDialog = () =>{
  if(getActiveProfile()?.type != 2) return;
  dialog.value = true
}
</script>

<template>
  <!-- Karta długu -->
  <AppCard
    class="background-card"
    no-padding
    bg-transparent
    :elevation="0"
    cols="12"
    @click="openDialog"
    style="cursor: pointer"
  >
    <v-card-text>
      <v-row justify="space-between" align="center">
        <!-- Tytuł -->
        <v-col>
          <div class="text-h6 font-weight-bold">
            {{ props.debt.name }}
          </div>
        </v-col>

        <!-- Kwota -->
        <v-col class="text-end" v-if = "getActiveProfile()?.type != 1">
          <div class="text-h5 font-weight-bold">
            {{ props.debt.amount }} {{ props.debt.currency }}
          </div>
          <div class="text-caption text-medium-emphasis">
            ({{ props.debt.amount_in_pln }} PLN)
          </div>
        </v-col>
        <v-col class="text-end" v-else>
          <div class="text-h5 font-weight-bold">
            {{ props.debt.amount_per_member }} {{ props.debt.currency }}
          </div>
          <div class="text-caption text-medium-emphasis">
            ({{ props.debt.amount_per_member_in_pln }} PLN)
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </AppCard>

  <!-- Dialog z uczestnikami -->
  <v-dialog v-model="dialog" max-width="600" class="pa-4">
    <v-card class="pa-4">
      <v-card-title class="text-h6 font-weight-bold">
        Czy uczestnik zapłacił?
      </v-card-title>
      <v-card-text>
        <v-row
          dense
          v-for="member in props.debt.members"
          :key="member.id"
          class="align-center mb-3"
        >
          <v-col cols="12" sm="8">
            <div class="font-weight-medium">
              {{ member.first_name }} {{ member.last_name }}
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ member.email }}
            </div>
          </v-col>
          <v-col cols="12" sm="4" class="text-sm-end text-start">
            <v-btn
              color="success"
              variant="tonal"
              icon="mdi-check"
              size="small"
              @click="markAsPaid(member.id)"
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Zamknij</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.background-card {
  background-color: rgb(var(--v-theme-background));
}
</style>
