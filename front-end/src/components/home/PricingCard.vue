<script setup lang="ts">
import AppButton from "@/components/budget/AppButton.vue";
import { PricingCard } from "@/types/interface";

const props = defineProps<PricingCard>();
console.log("PricingCard", props);
</script>

<template>
  <v-card
    :class="['pricing-card', contentVariant ?? buttonVariant]"
    class="d-flex flex-column align-center pa-6 w-100"
    :style="{ width: '280px' }"
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

    <v-list class="pricing-card__features mb-8" style="background-color: transparent; box-shadow: none;">
      <v-list-item
        v-for="(feature, idx) in features"
        :key="idx"
        class="justify-center py-1"
        
      >
        <v-icon size="22" class="checkmark me-2 ">mdi-check</v-icon>
        <span :class="contentVariant">{{ feature }}</span>
      </v-list-item>
    </v-list>

    <AppButton :variant="buttonVariant">Wybierz</AppButton>
  </v-card>
</template>

<style scoped lang="scss">
.pricing-card {
  background-color: rgba(var(--v-theme-secondary), 0.3);
  border-radius: 20px;
  text-align: center;
  transition: transform 0.3s ease;

  &.primary {
    background-color: rgba(var(--v-theme-primary), 0.6);
    color: white;

    .checkmark {
      color: rgb(var(--v-theme-secondary));
    }
  }

  &.secondary {
    background-color: rgba(var(--v-theme-secondary), 0.8);

    .checkmark {
      color: rgb(var(--v-theme-primary));
    }
  }

  &__name {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  &__price {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  &__features {
    list-style: none;
    padding: 0;

    .v-list-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 1rem;
    }
  }
}
</style>
