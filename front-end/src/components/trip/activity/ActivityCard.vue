<script setup lang="ts">
import { computed } from "vue";
import { useActivityStore } from "@/stores/trip/useActivityStore";

const props = defineProps({
  activity: {
    type: Object,
    required: true,
  },
});

const store = useActivityStore();

const getTypeLabel = (type: string) => {
  const found = store.activityTypes.find((t) => t.value === type);
  return found ? found.label : type;
};
</script>

<template>
  <v-card class="activity-card">
    <div class="activity-header">
      <div class="activity-info">
        <div class="activity-title">{{ activity.name }}</div>
        <div class="activity-description">{{ activity.description }}</div>
        <div class="activity-meta">
          <span class="activity-type">{{ getTypeLabel(activity.type) }}</span>
          <v-icon size="16" class="mx-1">mdi-clock-outline</v-icon> {{ activity.startTime }}
          <v-icon size="16" class="mx-1">mdi-timer-outline</v-icon> {{ activity.duration }}
          <v-icon size="16" class="mx-1">mdi-map-marker-outline</v-icon> {{ activity.location }}
        </div>
      </div>
      <v-btn icon color="#E44A3E" variant="text">
        <v-icon size="32">mdi-trash-can-outline</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<style scoped lang="scss">
.activity-card {
  background-color: rgb(var(--v-theme-background));
  border-radius: 1rem;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);

  .activity-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .activity-info {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .activity-title {
    font-weight: 600;
    font-size: 1rem;
    color: rgb(var(--v-theme-text));
  }

  .activity-description {
    font-size: 0.9rem;
    color: rgba(var(--v-theme-text),0.75);
  }

  .activity-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    font-size: 0.85rem;
    gap: 0.25rem;
    color: rgb(var(--v-theme-text));
  }

  .activity-type {
    color: rgb(var(--v-theme-accent));
    font-weight: 500;
  }
}
</style>