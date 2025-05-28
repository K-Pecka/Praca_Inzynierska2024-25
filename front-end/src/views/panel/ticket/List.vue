<script setup lang="ts">
import {computed, ref} from "vue";
import {Section} from "@/components";
import {deleteTicket} from "@/api";
import {useTripStore} from "@/stores/trip/useTripStore";
import TicketForm from "@/components/trip/module/ticket/TicketForm.vue";
import AppButton from "@/components/AppButton.vue";
import {useUtilsStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";
import {images} from "@/data";
import axios from "axios";

const {getTripId} = useUtilsStore();
const tripStore = useTripStore();
const {ticket} = tripStore;
const {getTickets, createTicket} = ticket;
const {
  data: tickets,
  isLoading,
  refetch: refetchTickets
} = getTickets(String(getTripId()));
import {useAuthStore} from "@/stores"
const {userData} = useAuthStore();
const {isOwner} = userData;

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

const handleDeleteTicket = async (ticketId: number) => {
  try {
    await deleteTicket({
      tripId: String(getTripId()),
      ticketId: String(ticketId),
    });

    await refetchTickets();
  } catch (error) {
  }
};

const downloadItem = async (url: string) => {
  const response = await axios.get(url, {responseType: "blob"});
  const blob = new Blob([response.data], {type: response.headers['content-type']});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "Bilet.jpeg";
  link.click();
  URL.revokeObjectURL(link.href);
}

const filteredTickets = () => {
  return (
      tickets.value?.filter((ticket) => ticket.trip === Number(getTripId())) ?? []
  );
};

const toggleForm = () => {
  showForm.value = !showForm.value;
};
import {useSafeDelete} from "@/composables/useSafeDelete";
const {confirmAndRun} = useSafeDelete();
const handleDelete = (trip: number) => {
  confirmAndRun(() => {
    handleDeleteTicket(trip);
  }, {
    title: "Potwierdź usunięcie biletu",
    message: "Czy na pewno chcesz usunąć ten bilet? Tego działania nie można cofnąć.",
    wordToConfirm: "USUŃ"
  });
};
const hasPermissionToDelete = () => {
  return isOwner(trip.value?.creator?.id ?? 0);
};
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
                    @click="showForm = true"
                />
              </v-row>
            </v-col>
          </template>


          <!-- Ticket -->
          <v-card
              class="background-secondary rounded-lg mb-6 w-100 pa-4"
              v-else-if="tickets && tickets.length > 0"
              v-for="ticket in filteredTickets().reverse()"
              :key="ticket.id"
              elevation="4"
          >
            <v-card-text>


              <!-- Icon with text -->
              <v-row justify="center">
                <v-col cols="12" xs="12" sm="8" md="5" lg="5">
                  <v-row class="h-100" align="center" justify="center" no-gutters>
                    <v-icon class="color-text" large size="70px" color="primary"> mdi-ticket</v-icon>
                    <v-row no-gutters class="flex-column justify-center pl-4">
                      <span class="color-text font-weight-bold text-h5">{{ ticket.name }}</span>
                      <span class="color-primary text-h6 font-weight-medium"
                            v-if="ticket.valid_from_date && ticket.valid_from_time">
                        {{ ticket.valid_from_time }} {{ ticket.valid_from_date }}
                      </span>
                    </v-row>
                  </v-row>
                </v-col>


                <!-- Select -->
                <v-col cols="12" xs="12" sm="8" md="4" lg="4">
                  <v-row align="center" justify="center" class="h-100" no-gutters>
                    <v-select
                        :items="members"
                        :disabled="members.length === 0"
                        label="Przypisz do osoby (Opcjonalnie)"
                        variant="outlined"
                        multiple
                        item-title="name"
                        item-value="userId"
                        density="compact"
                        bg-color="background"
                        rounded="lg"
                    />
                  </v-row>
                </v-col>


                <!-- Buttons -->
                <v-col cols="12" xs="12" sm="8" md="3" lg="3">
                  <v-row justify="end" align="center" class="h-100" no-gutters>
                    <v-col
                        cols="6"
                        sm="6"
                        md="12"
                        lg="12"
                        :class="$vuetify.display.smAndDown ? 'text-start' : 'text-end'">
                      <AppButton
                          color="primary-outline"
                          @click="() => downloadItem(ticket.file)"
                          font-auto
                          max-width="190px"
                          text="Pobierz bilet"
                      />
                    </v-col>
                    <v-col cols="6" sm="6" md="12" lg="12" class="text-end">
                      <AppButton
                          color="red"
                          @click="hasPermissionToDelete()
                            ? handleDelete(ticket.id)
                            : () => {}"
                          :disabled="!hasPermissionToDelete()"
                          font-auto
                          max-width="190px"
                          text="Usuń bilet"
                      />
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
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
