<script setup lang="ts">
import ParticipantItem from "./ParticipantItem.vue";
import {User} from "@/types";

const props = defineProps<{
  participants: User[];
}>();

const emit = defineEmits<{
  (e: "remove", id: number): void;
}>();

function handleRemove(id: number) {
  emit("remove", id);
}
</script>

<template>
  <v-col cols="12 mt-4">
    <v-row class="flex-column ga-5">
      <ParticipantItem
          v-for="participant in participants"
          :key="participant.userId"
          :user="participant"
          @remove="handleRemove"
      />
    </v-row>
  </v-col>
</template>

<style scoped lang="scss">
</style>
