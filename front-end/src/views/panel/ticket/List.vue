<script setup lang="ts">
import {computed, ref, watch} from "vue";
import {Section} from "@/components";
import {useTripStore} from "@/stores/trip/useTripStore";
import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/AppButton.vue";
import {useUtilsStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";
import {images} from "@/data";
import TicketCard from "@/components/trip/module/ticket/TicketCard.vue"

import {useAuthStore} from "@/stores"
const {userData} = useAuthStore();
const {isOwner} = userData;
const {getTripId} = useUtilsStore();
const tripStore = useTripStore();
const {ticket} = tripStore;
const {getTickets, createTicket} = ticket;
const {
  data: tickets,
  isLoading,
  refetch: refetchTickets
} = getTickets(String(getTripId()));


const {getTripDetails} = tripStore;
const {trip} = getTripDetails();
import {useMembersStore} from "@/stores/trip/useMembersStore"

const {setData} = useMembersStore();

const members = computed(() => {
  if (trip.value !== undefined) {
    setData(trip.value);
  }
  return useMembersStore().members.filter(e => !e.is_owner && !e.is_guest) || [];
});
const showForm = ref(false);

async function handleAddTicket(newTicketData: {
  type: string | number;
  name: string;
  date: string;
  time: string;
  assignedTo?: (string | number)[];
  file: File;
}) {
  const formData = new FormData();

  formData.append("type", String(newTicketData.type));
  formData.append("name", newTicketData.name);
  formData.append("trip", String(getTripId()));
  formData.append("valid_from_date", newTicketData.date);
  formData.append("valid_from_time", newTicketData.time);
  if (newTicketData.file){
    formData.append("file", newTicketData.file);
  }

  if (newTicketData.assignedTo?.length) {
    newTicketData.assignedTo.forEach((id) => {
      formData.append("profiles", String(id));
    });
  }

  try {
    createTicket.mutate(
      {
        formData,
        params: { tripId: String(getTripId()) }
      }
    );
    await refetchTickets();
    showForm.value = false;
  } catch (error: any) {
    console.error("Error creating ticket:", error.response?.data || error.message);
  }
}

const filteredTickets = () => {
  return (
      tickets.value?.filter((ticket) => ticket.trip === Number(getTripId())) ?? []
  );
};

const toggleForm = () => {
  showForm.value = !showForm.value;
};

const addTicket = () => {
  if (isOwner(trip.value?.creator?.id ?? 0)) {
    showForm.value = true
  }
}
const selectedMembers = ref(trip.value?.members);

</script>

<template>
  <Section>
    <template #title v-if="(tickets && tickets.length > 0) || showForm">
      <HeaderSection
          subtitle="Bilety"
          :button="isOwner(trip?.creator?.id ?? 0)"
          button-text="Dodaj Bilet"
          :button-action="toggleForm"
      />
    </template>

    <template #content>

      <!-- Ticket create form -->
      <v-col cols="12" class="pa-0 mb-5" v-if="showForm">
        <TicketForm
            :members="members"
            @submitTicket="handleAddTicket"
            @cancelForm="showForm = false"
            class="form-container"
        />
      </v-col>

      <!-- Ticket cards -->
      <v-col cols="12">
        <v-row>
          <!-- Empty state when no tickets are present -->
          <template v-if="!isLoading && tickets && tickets.length === 0 && !showForm">
            <v-col cols="12" class="py-10">
              <v-row justify="center" align="center" class="flex-column text-center">
              <span class="empty-header font-weight-bold mb-8">
              Nie masz jeszcze żadnych biletów
              </span>
                <v-img
                    :src="images.emptyState.ticket.img"
                    :alt="images.emptyState.ticket.alt"
                    class="empty-plan-image mb-6"
                    aspect-ratio="1"
                    contain
                />
                <AppButton
                    color="primary"
                    class="plan-button"
                    width="300px"
                    height="height-auto"
                    fontSize="font-auto"
                    text="Dodaj bilet"
                    :disabled="!isOwner(trip?.creator?.id ?? 0)"
                     @click="addTicket"
                />
              </v-row>
            </v-col>
          </template>
          <TicketCard
            v-else-if="tickets && tickets.length > 0"
            :ticket="ticket"
            v-for="ticket in filteredTickets().reverse()"
            :key="ticket.id"
            :members="members"
            :creatorId="trip?.creator?.id ?? 0"
            :refetchTickets="refetchTickets"
          />
          <!-- Ticket -->
          
        </v-row>
      </v-col>
    </template>
  </Section>
</template>

<style lang="scss">
@use "@/assets/styles/variables" as *;
.v-select .v-input__details {
  position: absolute;
}

.empty-header {
  font-size: clamp(0.3em, 1.5vw + 0.5em, 1.5em);
  color: rgb($primary-color);
}

.empty-plan-image {
  width: clamp(15em, 15vw + 10em, 25em);
  height: auto;
}
</style>
