<script setup lang="ts">
import {useActivityStore} from "@/stores/trip/useActivityStore";

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

const formatDuration = (minutes: string | number | null) => {
  if (!minutes || Number(minutes) === 0) return "";

  const totalMinutes = Number(minutes);
  const hours = Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;

  if (hours > 0 && mins > 0) {
    return `${hours}h ${mins}m`;
  } else if (hours > 0) {
    return `${hours}h`;
  } else {
    return `${mins}m`;
  }
};

const formatTime = (timeString: string) => {
  if (!timeString) return "";
  return timeString.slice(0, 5);
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

        <template v-if="activity.start_time">
          <span class="icon-text-pair">
            <v-icon size="16">mdi-clock-outline</v-icon>
            {{ formatTime(activity.start_time) }}
          </span>
        </template>

        <template v-if="activity.duration">
          <span class="icon-text-pair">
            <v-icon size="16">mdi-timer-outline</v-icon>
            {{ formatDuration(activity.duration) }}
          </span>
        </template>

        <template v-if="activity.location">
          <span class="icon-text-pair">
            <v-icon size="16">mdi-map-marker-outline</v-icon>
            {{ activity.location }}
          </span>
        </template>
      </div>
    </div>

    <v-btn icon variant="text" color="#E44A3E" class="delete-btn">
      <v-icon size="32">mdi-trash-can-outline</v-icon>
    </v-btn>
  </div>
</v-card>

</template>

<style scoped lang="scss">
.activity-card {
  background-color: rgb(var(--v-theme-background));
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  box-sizing: border-box;
  position: relative;

  .activity-header {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .activity-info {
    flex: 1;
  }

  .activity-title {
    font-weight: 600;
    font-size: clamp(1rem, 1.5vw, 1.15rem);
    color: rgb(var(--v-theme-text));
  }

  .activity-description {
    font-size: clamp(0.85rem, 1.4vw, 1rem);
    color: rgba(var(--v-theme-text), 0.75);
  }

  .activity-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    font-size: clamp(0.75rem, 1.2vw, 0.9rem);
    color: rgb(var(--v-theme-text));

    .v-icon {
      color: rgba(3, 3, 9, 0.7);
    }
  }

  .icon-text-pair {
    display: flex;
    align-items: center;
    white-space: nowrap;
    gap: 5px;
  }

  .activity-type {
    color: rgb(var(--v-theme-accent));
    font-weight: 500;
  }

}

</style>