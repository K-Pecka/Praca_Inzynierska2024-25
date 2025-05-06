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
  buttonAction?: () => void;
}>();
</script>

<template>
  <v-col cols="12">
    <v-row class="flex-column">
      <v-col cols="12" class="title font-weight-bold color-text">
        <span v-if="!isLoading_trip && !error_trip">
          {{ trip?.name }}
        </span>
        <span v-else>
          ...
        </span>
      </v-col>
      <v-col cols="12 justify-space-between">
        <v-row class="justify-space-between" no-gutters>
          <span class="text-h5" v-if="!noSubTitle && subtitle">
            {{ subtitle }}
          </span>
          <span v-else>
            ...
          </span>
          <AppButton
              v-if="!noSubTitle && button"
              variant="primary"
              @click="buttonAction"
              dense
              height-auto
              font-auto
              :text="buttonText"
          />
        </v-row>
      </v-col>
    </v-row>
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.title {
  font-size: $header-section-title-font-size;
}
</style>