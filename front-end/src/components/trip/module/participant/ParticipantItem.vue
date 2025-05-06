<script setup lang="ts">
import { User } from "@/types";

const props = defineProps<{
  user: User;
}>();

const emit = defineEmits(["remove"]);

function handleRemoveClick() {
  emit("remove", props.user.userId);
}

const tags = [
  {
    name: "Oczekujący",
    color: "orange-darken-2",
    condition: props.user.is_guest === true,
  },
  {
    name: "Potwierdzony",
    color: "green",
    condition: props.user.is_guest === false,
  },
];
</script>

<template>
  <v-sheet
    class="participant-item"
    :class="{ 'participant-item--noactive': user.is_guest }"
  >
    <v-container>
      <v-row class="participant-left" align="center" no-gutters>
        <v-col class="participant-texts">
          <v-sheet color="transparent">
            <v-icon size="48">mdi-account-outline</v-icon>
          </v-sheet>
          <v-sheet color="transparent">
            <span class="participant-name">{{ user.name }}</span>
            <v-row class="email-row" align="center" no-gutters>
              <v-icon size="18" color="#555">mdi-email-outline</v-icon>
              <span class="participant-email">{{ user.email }}</span>
            </v-row>
          </v-sheet>
        </v-col>

        <v-row class="tags-row" no-gutters>
          <v-col
            v-for="tag in tags.filter((tag) => tag.condition)"
            :key="tag.name"
            cols="auto"
          >
            <v-chip
              variant="outlined"
              size="medium"
              class="status-chip text-center justify-center"
              :color="tag.color"
            >
              {{ tag.name }}
            </v-chip>
          </v-col>
        </v-row>
      </v-row>
    </v-container>
    <v-btn class="delete-button" @click="handleRemoveClick">
      <v-icon size="24">mdi-trash-can-outline</v-icon>
    </v-btn>
  </v-sheet>
</template>

<style scoped lang="scss">
.participant-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgb(var(--v-theme-background));
  border-radius: 12px;
}

.participant-item--noactive {
  background-color: rgba(var(--v-theme-background),0.6);
}

.participant-left {
  display: flex;
  align-items: flex-start;
  flex-direction: row;
  gap: 0.5rem;
  width: 80%;
}
.participant-texts {
  display: flex;
  flex-direction: row;
  width: 40%;
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
  margin-bottom: 2px;
}

.tags-row {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.status-chip {
  text-align: center;
  min-width: 120px;
}

.delete-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #e44a3e;
  display: flex;
  align-items: center;
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.8;
  }
}
</style>
