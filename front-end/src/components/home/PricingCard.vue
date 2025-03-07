<script setup lang="ts">
import AppButton from "@/components/budget/AppButton.vue";
import { PricingCard } from "@/type/interface";

defineProps<PricingCard>();
</script>

<template>
  <div class="pricing-card" :class="buttonVariant">
    <h2 class="pricing-card__name">{{ name }}</h2>
    <p class="pricing-card__price">{{ price }}</p>

    <ul class="pricing-card__features">
      <li v-for="(feature, idx) in features" :key="idx">
        <v-icon size="22" class="checkmark">mdi-check</v-icon>
        <span>{{ feature }}</span>
      </li>
    </ul>

    <AppButton :variant="buttonVariant">Wybierz</AppButton>
  </div>
</template>

<style scoped lang="scss">
.pricing-card {
  background-color: rgba(var(--v-theme-secondary),0.3);
  padding: 2rem 1.5rem;
  border-radius: 20px;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  text-align: center;
  transition: transform 0.3s ease;
  width: 280px;

  &.primary {
    background-color: rgba(var(--v-theme-primary),0.6);
    color: white;
    transform: scale(1);

    .checkmark {
      color: rgb(var(--v-theme-secondary));
    }

  }

  &.secondary {
    background-color: rgba(var(--v-theme-secondary),0.8);
    transform: scale(1);

    .checkmark {
      color: rgb(var(--v-theme-primary));
    }
    .app-button {
      background-color: rgba(var(--v-theme-primary), 0.15);
      color: rgb(var(--v-theme-primary));
      &:hover {
        background-color: rgba(var(--v-theme-primary), 0.25);
      }
    }
  }

  &__name {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }

  &__price {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  &__features {
    list-style: none;
    padding: 0;
    margin-bottom: 2rem;

    li {
      margin: 0.5rem 0;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      font-size: 1rem;
    }
  }
}
</style>
