<script setup lang="ts">
import {computed, ref} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import AppButton from "@/components/budget/AppButton.vue";
import ParticipantList from "@/components/trip/module/participant/ParticipantList.vue";
import ParticipantsCounter from "@/components/trip/module/participant/ParticipantsCounter.vue";
import ParticipantAddForm from "@/components/trip/module/participant/ParticipantAddForm.vue";
import {Participant} from "@/types";
import {useTripStore, useNotificationStore} from "@/stores";
import HeaderSection from "@/components/common/HeaderSection.vue";

const {setErrorCurrentMessage} = useNotificationStore();
const route = useRoute();
const tripId = Number(route.params.tripId);

const {getTripDetails, removeParticipant, addParticipant} = useTripStore();
const {data: tripData, isLoading, error} = getTripDetails(tripId);
const participants = computed<Participant[]>(() => {
  if (!tripData.value) return [];

  return [
    ...tripData.value?.members ?? [],
    ...tripData.value?.pending_members ?? []
  ];
});

const maxParticipants = 5;

const showForm = ref(false);

function inviteParticipant(participant: { name: string; email: string }) {
  if (participants.value.length == maxParticipants) {
    setErrorCurrentMessage("Osiągnięto limit");
    return;
  }
  addParticipant(Number(tripId), participant);
}

function removeParticipantById(id: number) {
  removeParticipant(Number(tripId), id);
}

const toggleForm = () => {
  showForm.value = !showForm.value;
};
</script>

<template>
  <div class="page-container">
    <Section>
      <template #title>
        <HeaderSection
            subtitle="Zarządzaj uczestnikami"
            button
            button-text="Dodaj"
            :button-action="toggleForm"
        />
      </template>

      <template #content>
        <v-container class="page-container" fluid>
          <v-row>
            <v-col>
              <ParticipantsCounter
                  :current="participants.length"
                  :max="maxParticipants"
                  title="Uczestnicy"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <ParticipantAddForm
                  v-if="showForm"
                  title="Dodaj uczestnika"
                  @cancel="showForm = false"
                  @submitForm="inviteParticipant"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <div class="participants-card">
                <h3 class="card-title">Dodani uczestnicy</h3>

                <ParticipantList
                    :participants="participants"
                    @remove="removeParticipantById"
                />
              </div>
            </v-col>
          </v-row>
        </v-container>
      </template>
    </Section>
  </div>
</template>

<style scoped lang="scss">
.header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.title-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.sub-title {
  font-size: 2rem;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.participants-card {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.card-title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
}

</style>
