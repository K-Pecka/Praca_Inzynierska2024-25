<script setup lang="ts">
import ParticipantItem from "./ParticipantItem.vue";
import { User } from "@/types";

const props = defineProps<{
  participants: User[];
}>();

const emit = defineEmits<{
  (e: "remove", id: number): void;
}>();

function handleRemove(id: number) {
  emit("remove", id); 
}

//console.log(props.participants)
</script>

<template>
  <div class="participant-list">
    <ParticipantItem
        v-for="participant in participants"
        :key="participant.userId"
        :user="participant"
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
