<script setup lang="ts">
import {useDisplay} from 'vuetify'

import {pricingPlans} from "@/data/page/home";
import PricingCard from "@/components/home/PricingCard.vue";
import Section from "../../../components/common/Section.vue";
import {HeaderSection} from "@/components";

const {smAndDown} = useDisplay()

</script>

<template>
  <Section class="pb-10">
    <template #title>
    <HeaderSection
        title="Wybierz plan"
        subtitle="Wybierz plan, który najlepiej odpowiada Twoim potrzebom."
        center
    />
    </template>

    <template #content>
      <v-col cols="7">
        <v-row justify="center">
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
          <router-link :to="{ name: 'contactUs' }">Skontaktuj się</router-link>
          z nami!
        </p>
      </v-col>
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
