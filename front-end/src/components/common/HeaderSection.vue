<script setup lang="ts">
import {useRoute} from "vue-router";
import {useTripStore} from "@/stores";
import AppButton from "@/components/AppButton.vue";

const route = useRoute();
const tripId = Number(route.params.tripId);
const {getTripDetails} = useTripStore();
const {trip, isLoading_trip, error_trip} = getTripDetails(tripId);

defineProps<{
  subtitle?: string;
  noSubTitle?: boolean;
  button?: boolean;
  buttonText?: string;
  titleGradientText?: string;
  buttonAction?: () => void;
  title?: string;
  center?: boolean;
}>();
</script>

<template>
  <v-row class="flex-column" justify="center">

    <!-- Title -->
    <v-col>
      <v-row :class="{ 'justify-center': center }" class="title color-text" no-gutters>
          <span v-if="!isLoading_trip && !error_trip && !title">
            {{ trip?.name }}
          </span>
        <span v-else-if="!isLoading_trip && !error_trip" class="color-primary text-h3 font-weight-bold">
            {{ title }}
          </span>
        <span v-else>
            ...
        </span>
        <span v-if="titleGradientText" class="gradient-text text-h3 font-weight-bold">
          &nbsp;{{ titleGradientText }}
        </span>
      </v-row>
    </v-col>

    <!-- Subtitle -->
    <v-col v-if="!noSubTitle">
      <v-row :class="center ? 'justify-center' : 'justify-space-between'" no-gutters>
          <span class="text-h4" v-if="subtitle">
            {{ subtitle }}
          </span>
        <span v-else>
            ...
          </span>
        <AppButton
            v-if="button"
            color="primary"
            @click="buttonAction"
            dense
            height-auto
            font-auto
            :text="buttonText"
        />
      </v-row>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.title {
  font-size: $header-section-title-font-size;
}
</style>