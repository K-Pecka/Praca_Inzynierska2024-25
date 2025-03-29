<script setup lang="ts">
import ActivityCard from "./ActivityCard.vue";
import type { Activity } from "@/stores/trip/useActivityStore";

const props = defineProps({
  activities: {
    type: Array as () => Activity[],
    default: () => [],
  },
});
</script>

<template>
  <div class="activity-list">
    <ActivityCard
        v-for="activity in activities"
        :key="activity.id"
        :activity="activity"
    />
  </div>
</template>

<style scoped lang="scss">
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
