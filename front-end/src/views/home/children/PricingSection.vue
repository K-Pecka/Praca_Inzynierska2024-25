<script setup lang="ts">
  import { useDisplay } from 'vuetify'

  import { pricingPlans } from "@/data/page/home";
  import PricingCard from "@/components/home/PricingCard.vue";

  const { smAndDown } = useDisplay()

</script>

<template>
  <span class="text-h4 pb-4 font-weight-bold text-center">Wybierz plan</span>
  <p class="text-h5" :class="{ 'text-center': smAndDown }">
    Wybierz plan, który najlepiej odpowiada Twoim potrzebom.
  </p>

  <v-col cols="12">
    <v-row justify="center" class="mx-auto py-10" style="max-width: 1200px;">
      <v-col
        v-for="(plan, index) in pricingPlans"
        :key="plan.name"
        cols="12"
        sm="6"
        md="4"
      >
        <v-fade-transition>
          <PricingCard
            :name="plan.name"
            :price="plan.price"
            :features="plan.features"
            :button-variant="plan.buttonVariant"
            :content-variant="plan.contentVariant"
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
    <router-link :to="{ name: 'contactUs' }" class="hover-primary">Skontaktuj się</router-link> z nami!
  </p>
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.text-h4 {
  color: $primary-color;
}

.middle-card-color {
  background-color: $button-background-primary;
  color: white;
}

.default-card-color {
  background-color: $button-background-secondary;
}
</style>
