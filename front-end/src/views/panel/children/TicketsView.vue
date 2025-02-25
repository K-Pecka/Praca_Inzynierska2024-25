<script setup lang="ts">
import {ref, computed} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import {useTicketStore} from "@/stores/useTicketStore";
import TicketList from "@/components/trip/TicketList.vue";
import TicketForm from "@/components/trip/TicketForm.vue";

const route = useRoute();
const tripName = "Wakacje we Francji";

const ticketStore = useTicketStore();
const tickets = computed(() => ticketStore.tickets);

const showForm = ref(false);

function handleAddTicket(newTicketData: {
  type: string; name: string; date: string; assignedTo?: string; file?: File;
}) {
  ticketStore.addTicket(newTicketData);
  showForm.value = false;
}
</script>
<template>
  <Section>
    <template #title>
      <h1>{{ tripName }}</h1>
    </template>

    <template #content>
      <div class="d-flex align-center justify-end">
        <v-btn color="primary" @click="showForm = !showForm">
          Dodaj Bilet
        </v-btn>
      </div>

      <div v-if="tickets.length === 0 && !showForm" class="empty-tickets">
        <div class="empty-state">
          <v-icon size="48">mdi-ticket-confirmation</v-icon>
          <p>Brak dodanych biletów</p>
          <a @click="showForm = true">Dodaj pierwszy bilet</a>
        </div>
      </div>

      <TicketList v-else-if="tickets.length > 0" :tickets="tickets"/>

      <TicketForm
          v-if="showForm"
          @submitTicket="handleAddTicket"
          @cancelForm="showForm = false"
      />
    </template>
  </Section>
</template>


<style scoped lang="scss">
h1 {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.empty-tickets {
  padding: 2rem;
  background-color: rgb(var(--v-theme-secondary), 0.2);
  text-align: center;
  border-radius: 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-state img {
  width: 80px;
  height: auto;
}
</style>
