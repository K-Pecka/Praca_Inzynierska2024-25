<script setup lang="ts">
import { defineProps } from "vue";

interface Trip {
  title: string;
  location: string;
  dateRange: string;
  actions: {
    label: string;
    color: string;
    onClick: () => void;
  }[];
}

defineProps<{
  trips: Trip[];
}>();
</script>

<template>
  <v-container fluid class="trip-container">
    <v-row :gap="6.25">
      <v-col
        v-for="(trip, index) in trips"
        :key="index"
        cols="12"
        sm="6"
        md="6"
        lg="6"
      >
        <v-card class="trip-card pa-4" elevation="3">
          <v-card-title class="text-h6 font-weight-medium text-center">
            {{ trip.title }}
          </v-card-title>

          <v-card-subtitle class="text-center">
            <v-icon class="mr-1">mdi-map-marker</v-icon> {{ trip.location }}
          </v-card-subtitle>

          <v-card-text class="text-center">
            {{ trip.dateRange }}
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn
              v-for="(action, i) in trip.actions"
              :key="i"
              :class="['action-btn', action.color]"
              class="action-btn"
              @click="action.onClick"
            >
              {{ action.label }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
.trip-container {
  padding: 16px;
}

.trip-card {
  border-radius: 16px;
  background-color: rgba(var(--v-theme-secondary), 0.5);
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}
button{
    width: 40%;
    border-radius: 0.5rem;
}
.action-btn {
  margin: 4px;
}
.v-card-actions{
    margin-top: 3rem;
}
.v-card-subtitle,.v-card-text{
    margin-top: 1.5rem;
}
</style>
