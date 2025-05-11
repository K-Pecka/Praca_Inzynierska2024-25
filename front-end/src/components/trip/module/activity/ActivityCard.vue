<script setup lang="ts">
import {useActivityStore} from "@/stores/trip/useActivityStore";
import {useAuthStore, useUtilsStore} from "@/stores";

const {getTripId, getPlanId} = useUtilsStore();
import AppButton from "../../../AppButton.vue";

defineProps({
  isOwner: Boolean,
  activity: {
    type: Object,
    required: true,
  },
});

const {activityTypes, deleteActivity} = useActivityStore();

const getTypeLabel = (type: number | string) => {
  const typeAsNumber = Number(type);
  const found = activityTypes.find((t) => t.id === typeAsNumber);
  return found ? found.name : String(type);
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
          <v-col cols="12" sm="6" md="8" lg="8">
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
          </v-col>
          <v-col cols="12" sm="6" md="4" lg="4" v-if="isOwner">
            <v-row no-gutters align="center" justify="end" class="h-100">
              <v-card-actions class="justify-end justify-sm-center">
                <AppButton
                    color="red"
                    font-auto
                    max-width="190px"
                    style="min-width: 150px;"
                    text="Usuń aktywność"
                    @click="() => {
                    deleteActivity.mutate({
                    activityId: String(activity.id),
                    tripId: String(getTripId()),
                    planId: String(getPlanId())
                  })}"
                />
              </v-card-actions>
            </v-row>
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