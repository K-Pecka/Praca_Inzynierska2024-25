<script setup lang="ts">
import {ref, computed} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import {useTripStore} from "@/stores/trip/useTripStore";
import TicketList from "@/components/trip/modul/ticket/TicketList.vue";
import TicketForm from "@/components/trip/modul/ticket/TicketForm.vue";
import AppButton from "@/components/budget/AppButton.vue";

const route = useRoute();
const tripId = route.params.tripId as string;

const {getTripDetails} = useTripStore();
const {data: tripData, isLoading, error} = getTripDetails(tripId);

const ticketStore = useTicketStore();
const tickets = computed(() => ticketStore.tickets);

const showForm = ref(false);

function handleAddTicket(newTicketData: {
  type: string; name: string; date: string; time: string; assignedTo?: string[]; file: File;
}) {
  const {file, ...ticketData} = newTicketData;
  //const {createTicket} = useTicketStore();
  //createTicket(file,ticketData);
  ticketStore.addTicket(newTicketData);
  showForm.value = false;
}
</script>

<template>
  <div class="page-container">
    <Section>
      <template #title>
        <div class="header-wrapper">
          <div class="title-container">
            <h1 class="trip-title" v-if="!isLoading && !error">{{ tripData?.name }}</h1>
            <h1 class="trip-title" v-else>Ładowanie nazwy wycieczki...</h1>
            <h1 class="section-title">Bilety</h1>
          </div>
          <div class="button-container">
            <AppButton
                variant="primary"
                size="md"
                class="add-button"
                @click="showForm = !showForm"
            >
              Dodaj Bilet
            </AppButton>
          </div>
        </div>
      </template>

      <template #content>
        <div class="content-container">
          <TicketForm
              v-if="showForm"
              @submitTicket="handleAddTicket"
              @cancelForm="showForm = false"
              class="form-container"
          />

          <div v-if="tickets.length === 0 && !showForm" class="empty-tickets">
            <div class="empty-state">
              <v-icon size="48" color="black">mdi-ticket-confirmation-outline</v-icon>
              <p class="empty-text">Brak dodanych biletów</p>
              <a class="add-link" @click="showForm = true">Dodaj pierwszy bilet</a>
            </div>
          </div>

          <TicketList v-else-if="tickets.length > 0" :tickets="tickets"/>

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

.empty-tickets {
  padding: 2rem;
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
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

.form-container {
  margin-bottom: 1rem;
}
</style>
