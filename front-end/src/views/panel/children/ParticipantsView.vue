<script setup lang="ts">
import {ref} from "vue";
import {useRoute} from "vue-router";
import {Section} from "@/components";
import AppButton from "@/components/budget/AppButton.vue";
import ParticipantList from "@/components/trip/ParticipantList.vue";
import ParticipantsCounter from "@/components/trip/ParticipantsCounter.vue";
import ParticipantAddForm from "@/components/trip/ParticipantAddForm.vue";
import {Participant} from "@/type";
import {useTripStore, useUtilStore} from "@/stores";


const route = useRoute();
const tripId = route.params.tripId as string;

const {getTripDetails} = useTripStore();
const {data: tripData, isLoading, error} = getTripDetails(tripId);

const participants = ref<Participant[]>([
  {
    id: "p1",
    name: "Mateusz Wiśniewski",
    email: "s24893@pjwstk.edu.pl",
    role: "przeglądanie",
  },
  {
    id: "p2",
    name: "Andrzej Ebertowski",
    email: "s25222@pjwstk.edu.pl",
    role: "przeglądanie",
  }
]);

const maxParticipants = 5;

const inviteEmail = ref();

const showForm = ref(false);

function inviteParticipant() {
  const {invateUserMutation} = useTripStore();
  invateUserMutation.mutateAsync(inviteEmail.value);
  const {getTripId} = useUtilStore()
  useTripStore().invateUserMutation.mutateAsync({userEmail: inviteEmail.value, param: {tripId: getTripId().value}});
}

function removeParticipantById(id: string) {
  participants.value = participants.value.filter(p => p.id !== id);
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
            <h2 class="second-title">Utwórz nowy plan</h2>
          </div>
          <div class="button-container">
            <AppButton
                variant="primary"
                size="md"
                @click="showForm = !showForm"
            >
              Dodaj uczestnika
            </AppButton>
          </div>
        </div>
      </template>

      <template #content>
        <ParticipantsCounter
            :current="participants.length"
            :max="maxParticipants"
            title="Uczestnicy"
        />

        <ParticipantAddForm
            v-if="showForm"
            title="Dodaj uczestnika"
            @cancel="showForm = false"
            @submitForm="inviteParticipant"
        />

        <div class="participants-card">
          <h3 class="card-title">Dodani uczestnicy</h3>

          <ParticipantList
              :participants="participants"
              @remove="removeParticipantById"
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

.second-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0;
}

.button-container {
  display: flex;
  align-self: flex-end;
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