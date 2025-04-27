<script setup lang="ts">
import { computed } from "vue";
import { useTicketStore } from "@/stores/trip/useTicketStore";
import AppButton from "@/components/budget/AppButton.vue";
import { TicketData } from "@/types";

const props = defineProps({
  ticket: {
    type: Object as () => TicketData,
    required: true,
  },
});

const store = useTicketStore();


function formatDate(dateString: string): string {
  return new Intl.DateTimeFormat("pl-PL").format(new Date(dateString));
}
const downloadFile = (ticket:string) => {
  const link = document.createElement('a');
  link.href = ticket;
  link.download = 'bilet.pdf';
  link.click();
}
</script>

<template>
  <v-card class="ticket-card">
    <div class="ticket-header">
      <v-icon class="ticket-icon" large> mdi-dowland</v-icon>
      <div class="ticket-header-text">
        <div class="ticket-name">{{ ticket.type_display }}</div>
        <div class="ticket-date" v-if="ticket.valid_from">
          {{  }}
        </div>
      </div>
    </div>

    <hr class="ticket-divider" />

    <div class="ticket-body">
      <v-select
        clearable
        chips
        
        :items="['Jan', 'Anna', 'Piotr']"
        label="Przypisz do osoby (Opcjonalnie)"
        variant="outlined"
        class="assign-select"
        multiple
        bg-color="background"
        density="comfortable"
      />
      <div class="ticket-btn-wrapper">
        <AppButton variant="primary" @click="() => downloadFile(ticket.file)">
          <v-icon>mdi-download</v-icon>Pobierz bilet
        </AppButton>
      </div>
    </div>
  </v-card>
</template>

<style scoped lang="scss">
.ticket-card {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 1rem;
  padding: 1rem 2rem;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);

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
    gap: 1rem;

    @media (max-width: 768px) {
      flex-direction: column;
      justify-items: flex-end;
      align-items: stretch;
    }

    .assign-select {
      max-width: 450px;
      @media (max-width: 768px) {
        max-width: 100%;
        width: 100%;
      }
    }

    .app-button {
      margin-bottom: 1rem;
    }

    .ticket-btn-wrapper {
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>
