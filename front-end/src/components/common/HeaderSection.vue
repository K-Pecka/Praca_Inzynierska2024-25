<script setup lang="ts">
import {useRoute} from "vue-router";
import {useTripStore} from "@/stores";
import AppButton from "@/components/AppButton.vue";
import {no} from "vuetify/locale";

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
  title?: string;
  center?: boolean;
}>();
</script>

<template>
  <v-col cols="12">
    <v-row class="flex-column">
      <v-col cols="12">
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
        </v-row>
      </v-col>
      <v-col cols="12 justify-space-between" v-if="!noSubTitle">
        <v-row :class="center ? 'justify-center' : 'justify-space-between'" no-gutters>
          <span class="text-h4" v-if="!noSubTitle && subtitle">
            {{ subtitle }}
          </span>
          <span v-else>
            ...
          </span>
          <AppButton
              v-if="!noSubTitle && button"
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
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.title {
  font-size: $header-section-title-font-size;
}
</style>