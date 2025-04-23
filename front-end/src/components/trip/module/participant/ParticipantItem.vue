<script setup lang="ts">
import { Participant} from "@/types";

const props = defineProps<Participant>();

const emit = defineEmits(["remove"]);

function handleRemoveClick() {
  emit("remove", props.id);
}
</script>

<template>
  <div class="participant-item" :class="{ 'participant-item--noactive': props.is_guest }">
    <div class="participant-left">
      <v-icon size="48">mdi-account-outline</v-icon>

      <div class="participant-texts">
        <strong class="participant-name">{{ props.name }}</strong>
        <div class="email-row">
          <v-icon size="18" color="#555">mdi-email-outline</v-icon>
          <span class="participant-email">{{ props.email }}</span>
        </div>
      </div>
    </div>

    <v-btn class="delete-button" @click="handleRemoveClick">
      <v-icon size="24">mdi-trash-can-outline</v-icon>
    </v-btn>
  </div>
</template>

<style scoped lang="scss">
.participant-email,.participant-name{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 10rem;
}
.participant-item--noactive{
  background-color: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
}
.participant-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  background-color: rgb(var(--v-theme-background));
  border-radius: 12px;
  padding: 1rem 1.5rem;

  border: 1px solid rgba(0, 0, 0, 0.1);
}

.participant-left {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.participant-texts {
  display: flex;
  flex-direction: column;
}

.participant-name {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.email-row {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.participant-email {
  font-size: 0.9rem;
  color: #555;
}

.delete-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #e44a3e; /* ! */;
  display: flex;
  align-items: center;
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.8;
  }
}
</style>
