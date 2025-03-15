<script setup lang="ts">
import { Participant} from "@/type";

const props = defineProps<Participant>();

const emit = defineEmits(["openMenu"]);

function handleMenuClick() {
  emit("openMenu", props.id);
}
</script>

<template>
  <div class="participant-item">
    <div class="participant-info">
      <strong class="participant-name">{{ props.name }}</strong>
      <span class="participant-email">{{ props.email }}</span>
      <span class="participant-role">{{ props.role }}</span>
    </div>
      <button class="menu-button" @click="handleMenuClick">
        <v-icon size="32">mdi-dots-vertical</v-icon>
      </button>
  </div>
</template>

<style scoped lang="scss">
.participant-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(var(--v-theme-secondary), 0.8);
  border-radius: 15px;
  padding: 1rem 2rem;
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 15rem;
  flex-grow: 1;
}

.participant-name {
  font-weight: bold;
}

.menu-button {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
