<script setup lang="ts">
import {defineProps} from "vue";

const props = defineProps<{
  current: number;
  max: number;
}>();
</script>

<template>
  <div class="participants-counter-card">
    <div class="counter-header">
      <div class="left">
        <v-icon size="24" color="primary">mdi-account-multiple-outline</v-icon>
        <span class="counter-title">Uczestnicy</span>
      </div>
      <span class="counter-value">
        {{ props.current }}/{{ props.max }}
      </span>
    </div>
    <v-progress-linear
        :model-value="(props.current / props.max) * 100"
        color="primary"
        height="12"
    />
  </div>
</template>

<style scoped lang="scss">
.participants-counter-card {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.counter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 0.5rem;
  align-items: center;
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
