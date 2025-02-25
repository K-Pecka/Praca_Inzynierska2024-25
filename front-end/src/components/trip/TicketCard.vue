<script setup lang="ts">
import {computed} from "vue";
import {defineProps} from "vue";
import {useTicketStore} from "@/stores/useTicketStore";

const props = defineProps({
  ticket: {
    type: Object,
    required: true,
  },
});

const store = useTicketStore();
const icon = computed(() => {
  const found = store.ticketTypes.find((t) => t.value === props.ticket.type);
  return found ? found.icon : "mdi-ticket";
});

function previewTicket() {
  alert(`Podgląd biletu: ${props.ticket.name}`);
}
</script>

<template>
  <v-card class="ticket-card">
    <div class="ticket-header">
      <v-icon class="ticket-icon" large>{{ icon }}</v-icon>
      <div class="ticket-header-text">
        <div class="ticket-name">{{ ticket.name }}</div>
        <div class="ticket-date" v-if="ticket.date">
          {{ ticket.date }}
        </div>
      </div>
    </div>

    <hr class="ticket-divider"/>

    <div class="ticket-body">
      <v-select
          v-model="ticket.assignedTo"
          :items="['Jan', 'Anna', 'Piotr']"
          label="Przypisz do osoby (Opcjonalnie)"
          outlined
          density="compact"
          class="assign-select"
      />
      <v-btn
          color="primary"
          class="ticket-preview-btn"
          @click="previewTicket"
      >
        Podgląd
      </v-btn>
    </div>
  </v-card>
</template>


<style scoped lang="scss">
.ticket-card {
  background-color: rgb(var(--v-theme-secondary), 0.8);
  border-radius: 1rem;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  .ticket-header {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .ticket-icon {
    font-size: 3rem;
    color: rgb(var(--v-theme-text));
  }

  .ticket-header-text {
    display: flex;
    flex-direction: column;
  }

  .ticket-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: rgb(var(--v-theme-text));
  }

  .ticket-date {
    font-size: 0.9rem;
    color: rgb(var(--v-theme-primary));
  }

  .ticket-divider {
    border: none;
    border-top: 1px solid rgba(0, 0, 0, 0.15);
    margin: 0.5rem 0;
  }

  .ticket-body {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .assign-select {
      max-width: 300px;
    }

    .ticket-preview-btn {
      font-weight: 600;
    }
  }
}
</style>
