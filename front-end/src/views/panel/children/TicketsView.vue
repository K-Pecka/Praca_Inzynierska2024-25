<script setup lang="ts">
import {ref, computed} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import TicketList from "@/components/trip/TicketList.vue";
import TicketForm from "@/components/trip/TicketForm.vue";

const route = useRoute();
const tripName = "Wakacje we Francji";

const ticketStore = useTicketStore();
const tickets = computed(() => ticketStore.tickets);

const showForm = ref(false);

function handleAddTicket(newTicketData: {
  type: string; name: string; date: string; assignedTo?: string; file: File;
}) {
  const {file, ...ticketData} = newTicketData;
  const {createTicket} = useTicketStore();
  createTicket(file,ticketData);
  //ticketStore.addTicket(newTicketData);
  showForm.value = false;
}
</script>

<template>
  <div class="page-container">
    <Section>
      <template #title>
        <div class="header-wrapper">
          <div class="title-container">
            <h1 class="trip-title">{{ tripName }}</h1>
            <h1 class="section-title">Bilety</h1>
          </div>
          <div class="button-container">
            <v-btn
                color="primary"
                @click="showForm = !showForm"
                class="add-button"
                depressed
            >
              Dodaj Bilet
            </v-btn>
          </div>
        </div>
      </template>

      <template #content>
        <div class="content-container">
          <div v-if="tickets.length === 0 && !showForm" class="empty-tickets">
            <div class="empty-state">
              <v-icon size="48" color="black">mdi-ticket-confirmation-outline</v-icon>
              <p class="empty-text">Brak dodanych biletów</p>
              <a class="add-link" @click="showForm = true">Dodaj pierwszy bilet</a>
            </div>
          </div>

          <TicketList v-else-if="tickets.length > 0" :tickets="tickets"/>

          <TicketForm
              v-if="showForm"
              @submitTicket="handleAddTicket"
              @cancelForm="showForm = false"
          />
        </div>
      </template>
    </Section>
  </div>
</template>


<style scoped lang="scss">
.page-container {
  max-width: 88rem;
  margin: 0 auto;
  padding-top: 0;
}

.header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  margin-top: 0;
}

.title-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.trip-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.2rem 0;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0;
}

.button-container {
  display: flex;
  align-self: flex-end;
}

.add-button {
  height: 40px;
  font-size: 16px;
  font-weight: 500;
  text-transform: none;
  border-radius: 15px;
  padding: 0 24px;
}

.empty-tickets {
  padding: 2rem;
  background-color: rgb(var(--v-theme-secondary),0.5);
  border-radius: 12px;
  text-align: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.add-link {
  color: rgb(var(--v-theme-primary));
  font-weight: 500;
  text-decoration: underline;
  cursor: pointer;

  &:hover {
    opacity: 0.8;
  }
}

</style>
