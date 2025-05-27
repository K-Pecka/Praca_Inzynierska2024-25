<script setup lang="ts">
import AppButton from "@/components/AppButton.vue";
import { PricingCard } from "@/types/interface";
import { PricingPlanType } from "@/types/types";

const props = defineProps<PricingCard>();
const paymentPlanIds: Record<PricingPlanType, string> = {
  tourist: "price_1RRymmB3a037ikFEaqDq2J8N",
  premium: "price_1RQV0aB3a037ikFEAEbdKvqx",
  guide: "price_1RQwW7B3a037ikFEidRPP1SS"
};
const emit = defineEmits<{
  (e: 'plan-selected', planId: string): void;
}>();

const handleSelectPlan = () => {
  emit('plan-selected', paymentPlanIds[props.type as PricingPlanType]);
};
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
        class="justify-center py-1"
      >
        <v-icon size="22" class="checkmark me-2 ">mdi-check</v-icon>
        <span :class="contentVariant">{{ feature }}</span>
      </v-list-item>
    </v-list>

    <AppButton
        :color="buttonVariant"
        :onClick="handleSelectPlan"
        max-width="150px"
        text="Wybierz"
    />
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
