<script setup lang="ts">
import {ref, computed} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import {useTicketStore} from "@/stores/trip/useTicketStore";
import {useTripStore} from "@/stores/trip/useTripStore";
import TicketList from "@/components/trip/module/ticket/TicketList.vue";
import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/budget/AppButton.vue";

const route = useRoute();
const tripId = route.params.tripId as string;

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
import HeaderSection from "@/components/common/HeaderSection.vue";
</script>

<template>
    <Section>
      <template #title>
            <HeaderSection>
              <template #subtitle>
                <div class="title-container pb-1 w-100">
                  <h2 class="trip-title mb-10" style="font-size: 30px; font-weight: 600; width: 80%;">Bilety</h2>
                 <AppButton
                variant="primary"
                size="md"
                class="add-button"
                v-if="!showForm"
                @click="showForm = !showForm"
            >
              Dodaj Bilet
            </AppButton>
                </div>

              </template>
              </HeaderSection>
      </template>

      <template #content>
        <div class="w-100">
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
</template>


<style scoped lang="scss">

.title-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
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
