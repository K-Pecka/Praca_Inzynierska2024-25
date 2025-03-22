<script setup lang="ts">
import ParticipantItem from "./ParticipantItem.vue";
import { Participant} from "@/type";

const props = defineProps<{
  participants: Participant[];
}>();

function handleRemove(id: string) {
  console.log("Usuwam uczestnika o id:", id);
}
</script>

<template>
  <div class="participant-list">
    <ParticipantItem
        v-for="participant in participants"
        :key="participant.id"
        v-bind="participant"
        @remove="handleRemove"
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
