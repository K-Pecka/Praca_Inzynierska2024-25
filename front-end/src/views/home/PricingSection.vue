<script setup lang="ts">
import { pricingPlans } from "@/data/page/home";
import PricingCard from "@/components/home/PricingCard.vue";
import Section from "@/components/shared/Section.vue";
import { HeaderSection } from "@/components";
import { useAuthStore } from "@/stores";
import { PricingPlanType } from "@/types/types";

const selectPaymentPlan = (priceId: string) => {
  useAuthStore().startCheckout.mutate(priceId);
};
</script>

<template>
  <Section class="pb-10">
    <template #title>
      <HeaderSection
        title="Wybierz"
        title-gradient-text="plan"
        subtitle="Wybierz plan, który najlepiej odpowiada Twoim potrzebom."
        center
      />
    </template>

    <template #content>
      <v-row justify="center">
        <v-col
          v-for="(plan, index) in pricingPlans"
          :key="plan.name"
          cols="12"
          md="6"
          lg="4"
          xl="3"
        >
          <v-fade-transition>
            <PricingCard
              @plan-selected="selectPaymentPlan"
              :name="plan.name"
              :price="plan.price"
              :features="plan.features"
              :button-variant="plan.buttonVariant"
              :content-variant="plan.contentVariant"
              :type="plan.type as PricingPlanType"
              :class="{
                'middle-card-color': index % 2 !== 0,
                'default-card-color': index % 2 === 0
              }"
            />
          </v-fade-transition>
        </v-col>
      </v-row>
      <p class="text-center my-6">
        Nie jesteś pewien, który plan wybrać?
        <router-link :to="{ name: 'contactUs' }">Skontaktuj się</router-link>
        z nami!
      </p>
    </template>
  </Section>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.text-h4 {
  color: rgb($primary-color);
}

.middle-card-color {
  background-color: $background-primary;
  color: white;
}

.default-card-color {
  background-color: $background-secondary;
}
</style>
