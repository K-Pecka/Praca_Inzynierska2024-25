<script setup lang="ts">

const props = defineProps<{
  current: number;
  max: number;
}>();
</script>

<template>
  <v-col cols="12" class="background-secondary rounded-lg pa-6">
    <v-row no-gutters>
      <v-col class="pb-5">
        <v-icon size="24" color="primary">mdi-account-multiple-outline</v-icon>
        <span class="counter-title">Uczestnicy</span>
      </v-col>
      <span class="counter-value">
        {{ props.current }}/{{ props.max }}
      </span>
    </v-row>
    <v-progress-linear
        :model-value="(props.current / props.max) * 100"
        height="12"
        rounded
        class="progress-color"
    />
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables.scss" as *;

.progress-color {
  color: $background-primary;
}

.counter-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.counter-value {
  font-size: 1.2rem;
  font-weight: 500;
}
</style>
