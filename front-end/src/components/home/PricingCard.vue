<script setup lang="ts">
import {AppButton} from "@/components";
import { PricingCard } from "@/types/interface";
import { PricingPlanType } from "@/types/types";
import { useAuthStore } from "@/stores";
const { userData } = useAuthStore();
const { getUser } = userData;
const props = defineProps<PricingCard>();
const paymentitineraryIds: Record<PricingPlanType, string> = {
  tourist: "price_1RQV0aB3a037ikFEAEbdKvqx",
  guide: "price_1RQwW7B3a037ikFEidRPP1SS",
};
const emit = defineEmits<{
  (e: "plan-selected", itineraryId: string): void;
}>();

const handleSelectPlan = () => {
  if(props.type)
  {
    emit("plan-selected", paymentitineraryIds[props.type as PricingPlanType]);
  }
};
const subscriptionPlan = getUser()?.subscription_plan ?? null;
const subscritpionActive = getUser()?.subscription_active;
</script>

<template>
  <v-card
    class="pricing-card d-flex flex-column align-center pa-6 w-100"
    elevation="4"
  >
    <v-card-title
      class="pricing-card__name text-h6 font-weight-bold text-center"
    >
      {{ name }}
    </v-card-title>

    <v-card-subtitle
      class="pricing-card__price text-center text-subtitle-2 mb-6"
    >
      {{ price }}
    </v-card-subtitle>

    <v-list class="pricing-card__features mb-8">
      <v-list-item
        v-for="(feature, idx) in features"
        :key="idx"
        class="justify-center py-1 align-center"
      >
        <span
          :class="contentVariant"
          class="d-flex justify-center align-center"
          >{{ feature }}</span
        >
      </v-list-item>
    </v-list>
    <template v-if="(subscritpionActive == false && props.type == null) || subscriptionPlan == props.type">
      <AppButton :color="buttonVariant" max-width="150px" text="Wybrany" />
    </template>
    <template v-else>
      <AppButton
        :color="buttonVariant"
        :onClick="handleSelectPlan"
        max-width="150px"
        text="Wybierz"
      />
    </template>
  </v-card>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.pricing-card {
  border-radius: 20px;
  &__features {
    background-color: transparent;
    box-shadow: none;
    color: inherit;
  }
}
</style>
