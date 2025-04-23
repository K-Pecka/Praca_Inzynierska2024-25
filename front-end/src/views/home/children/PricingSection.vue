<script setup lang="ts">
import { pricingPlans } from "@/data/page/home";
import PricingCard from "@/components/home/PricingCard.vue";
import { Section } from "@/components/common";
</script>

<template>
  <Section>
    <template #title>
      <h1 class="text-h4 font-weight-bold text-center">Wybierz plan</h1>
      <p class="text-center">
        Wybierz plan, który najlepiej odpowiada Twoim potrzebom.
      </p>
    </template>

    <template #content>
      <v-container fluid class="my-6">
        <v-row
          class="pricing-row"
          justify="center"
          no-gutters
        >
          <v-col
            v-for="(plan, index) in pricingPlans"
            :key="plan.name"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            class="d-flex px-4 mb-6"
          >
            <v-fade-transition>
              <div
                class="fade-in w-100 d-flex justify-center"
                :style="{ animationDelay: `${index * 100}ms` }"
              >
                <PricingCard
                  :name="plan.name"
                  :price="plan.price"
                  :features="plan.features"
                  :button-variant="plan.buttonVariant"
                  :content-variant="plan.contentVariant"
                />
              </div>
            </v-fade-transition>
          </v-col>
        </v-row>
      </v-container>
    </template>

    <template #footer>
      <p class="text-center my-6">
        Nie jesteś pewien, który plan wybrać?
        <router-link :to="{ name: 'contactUs' }" class="hover-primary">Skontaktuj się</router-link> z nami!
      </p>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.hover-primary:hover {
  color: rgba(var(--v-theme-primary));
}
.hover-primary:hover::after {
  width: 100%;
}
.hover-primary:hover {
  color: rgba(var(--v-theme-primary));
}
.hover-primary::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 0;
  width: 0;
  height: 1px; 
  background-color: rgba(var(--v-theme-primary));
  transition: width 1s ease;
}
.hover-primary {
  position: relative;
  color: inherit;
  transition: color 0.5s ease;
  text-decoration: underline;
}
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s ease forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
