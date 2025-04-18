<script setup lang="ts">
import { pricingPlans } from "@/dataStorage/page/home";
import PricingCard from "@/components/home/PricingCard.vue";

</script>

<template>
  <section class="pricing-section">
    <PricingCard
        v-for="plan in pricingPlans"
        :key="plan.name"
        :name="plan.name"
        :price="plan.price"
        :features="plan.features"
        :button-variant="plan.buttonVariant"
    />
  </section>
</template>

<style scoped lang="scss">
.pricing-section {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  padding: 8rem 1rem;
  align-items: flex-start;

  min-width: 60vh;
  margin: 0 auto;
}

</style>
