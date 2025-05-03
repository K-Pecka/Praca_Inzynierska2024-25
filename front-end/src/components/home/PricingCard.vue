<script setup lang="ts">
import AppButton from "@/components/budget/AppButton.vue";
import { PricingCard } from "@/types/interface";

defineProps<PricingCard>();
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
        :variant="buttonVariant"
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
