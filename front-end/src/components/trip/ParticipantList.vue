<script setup lang="ts">
import { defineProps } from "vue";
import ParticipantItem from "./ParticipantItem.vue";
import { Participant} from "@/type";

const props = defineProps<{
  participants: Participant[];
}>();

function handleOpenMenu(participantId: string) {
  console.log("openMenu w ParticipantList, userId:", participantId);
}
</script>

<template>
  <div class="participant-list">
    <ParticipantItem
        v-for="participant in participants"
        :key="participant.id"
        :id="participant.id"
        :name="participant.name"
        :email="participant.email"
        :role="participant.role"
        @openMenu="handleOpenMenu"
    />
  </div>
</template>

<style scoped lang="scss">
.participant-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
