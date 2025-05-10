<script setup lang="ts">
import {useActivity} from "@/stores/trip/useActivity";
defineProps({
  isOwner:Boolean,
  activity: {
    type: Object,
    required: true,
  },
});
console.log("h");
const {activityTypes} = useActivity();

const getTypeLabel = (type: number | string) => {
  // const typeAsNumber = Number(type);
  // const found = activityTypes.find((t) => t.id === typeAsNumber);
  // return found ? found.name : String(type);
  return "UNKNOW"
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
  <v-col cols="12" class="pb-2">
    <v-card class="activity-card w-100" elevation="0">
      <v-card-text>
        <v-row class="activity-header justify-space-between" no-gutters>
          <v-col :cols="isOwner ? 11 : 12">
            <v-sheet class="bg-transparent">
              <v-row no-gutters>
                <span class="activity-title font-weight-bold">{{ activity.name }}</span>
              </v-row>
              <v-row no-gutters class="pb-1">
                <span class="activity-description">{{ activity.description }}</span>
              </v-row>
              <v-row no-gutters class="ga-3">
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
              </v-row>
            </v-sheet>
          </v-col>
          <v-col cols="1" v-if="isOwner">
            <v-card-actions class="justify-end">
              <v-btn icon variant="text" color="#E44A3E" class="delete-btn">
                <v-icon size="32">mdi-trash-can-outline</v-icon>
              </v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-col>


</template>

<style scoped lang="scss">
.activity-card {
  background-color: rgb(var(--v-theme-background));
  border-radius: 15px;

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
    font-size: clamp(0.75rem, 1.2vw, 0.9rem);
    color: rgb(var(--v-theme-text));

    .v-icon {
      color: rgba(var(--v-theme-text), 0.7);
    }
  }

  .activity-type {
    color: rgb(var(--v-theme-accent));
    font-weight: 500;
  }

}

</style>