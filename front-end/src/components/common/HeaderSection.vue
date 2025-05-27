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
  goBackAction?: () => void;
  title?: string;
  center?: boolean;
  btnGoBack?: boolean;
}>();
</script>

<template>
  <v-row class="flex-column" justify="center">

    <!-- Title -->
    <v-col cols="12">
      <v-row :class="{ 'justify-center': center || $vuetify.display.smAndDown }" class="title color-text" no-gutters>
        <span v-if="!isLoading_trip && !error_trip && !title">
          {{ trip?.name }}
        </span>
        <span
            v-else-if="!isLoading_trip && !error_trip"
            class="d-flex align-center color-primary text-h3 font-weight-bold"
            :class="{ 'justify-center flex-column': center || $vuetify.display.smAndDown }"
        >
          <AppButton
                v-if="btnGoBack"
                color="primary"
                @click="goBackAction"
                maxWidth="40px"
                iconSize="24px"
                icon
                dense
                iconName="mdi-arrow-left"
                font-auto
                class="mr-md-4"
            />
          <span>{{ title }}</span>
        </span>
        <span v-else>
            ...
        </span>
        <span
            v-if="titleGradientText"
            class="gradient-text text-h3 font-weight-bold"
        >
            &nbsp;{{ titleGradientText }}
          </span>
      </v-row>
    </v-col>

    <!-- Subtitle -->
    <v-col v-if="!noSubTitle">
      <v-row
          :class="center ? 'justify-center' : 'justify-space-between'"
          no-gutters
      >
        <v-col
            cols="12"
            sm="12"
            md="6"
            lg="6"
            class="header-subtext-container"
        >
          <v-row
              :class="{ 'justify-center': $vuetify.display.smAndDown || center, 'mb-5': $vuetify.display.smAndDown}"
              no-gutters
          >
            <span class="text-h4" v-if="subtitle">
              {{ subtitle }}
            </span>
            <span v-else>
              ...
            </span>
          </v-row>
        </v-col>
        <v-col
            cols="12"
            sm="12"
            md="6"
            lg="6"
            :class="{'text-end': !$vuetify.display.smAndDown}"
            class="header-button-container"
            v-if="button"
        >
            <AppButton
                color="primary"
                @click="buttonAction"
                dense
                font-auto
                :text="buttonText"
            />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;
.header-subtext-container {
  @media (max-width: 959px) {
    width: 100%;
  }
}

.header-button-container {
  @media (max-width: 959px) {
    width: 100%;
  }
}

.title {
  font-size: $header-section-title-font-size;
}

</style>