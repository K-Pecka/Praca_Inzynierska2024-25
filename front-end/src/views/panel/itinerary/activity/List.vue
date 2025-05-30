<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {useActivityStore} from "@/stores/trip/useActivityStore";
import {useTripStore, useAuthStore} from "@/stores";
import {useUtilsStore} from "@/stores/utils/useUtilsStore";
import {Activity} from "@/types/interface";
import ActivityCard from "@/components/trip/module/activity/ActivityCard.vue";
import ActivityForm from "@/components/trip/module/activity/ActivityForm.vue";
import AppButton from "@/components/AppButton.vue";
import HeaderSection from "@/components/shared/HeaderSection.vue";
import {Section} from "@/components";
const route = useRoute();


const {itinerary,trip:tripStore} = useTripStore();

const {getItineraries} = itinerary
const {getTripDetails} = tripStore

const {userData} = useAuthStore();
const {formatDatePolish,getTripId,getItineraryId} = useUtilsStore();
const activityStore = useActivityStore();

const {itineraries} = getItineraries();
const {trip} = getTripDetails()
const {data: activities, isSuccess} = activityStore.getActivity();

const isOwnerValue = computed(() => {
  const creatorId = trip.value?.creator?.id;
  return creatorId !== undefined ? userData.isOwner(creatorId) : false;
});

// Wszystkie dni planu (dla właściciela)
const allDays = computed(() => {
  const itinerary = itineraries.value?.results.find(el=>el.id == getItineraryId())
  const from = itinerary?.start_date;
  const to = itinerary?.end_date;
  if (!from || !to) return [];

  const arr: string[] = [];
  const dt = new Date(from);
  const end = new Date(to);
  while (dt <= end) {
    arr.push(dt.toISOString().split("T")[0]);
    dt.setDate(dt.getDate() + 1);
  }
  return arr;
});

// Grupowanie aktywności wg dat
const activityByDate = computed(() => {
  if (!activities.value) return {};

  return activities.value.reduce((acc, activity) => {
    const date = activity.date || "";
    if (!acc[date]) acc[date] = [];
    acc[date].push({...activity, date});
    return acc;
  }, {} as Record<string, Activity[]>);
});

// Widoczne dni zależne od właściciela
const days = computed(() => {
  return isOwnerValue.value
      ? allDays.value
      : Object.keys(activityByDate.value).filter((day) => activityByDate.value[day]?.length > 0);
});

const showFormForDay = ref<string | null>(null);

function addActivity(day: string, activityData: any) {
  activityStore.addActivity(
      {
        ...activityData,
        date: day,
      },
      {
        tripId:String(getTripId()),
        itineraryId: String(getItineraryId()),
      }
  );
  showFormForDay.value = null;
}

onMounted(() => {
  activityStore.loadActivityTypes(String(getTripId()));
});
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection :subtitle="isOwnerValue ?'Zarządzaj aktywnościami':'Aktualne aktywności'"/>
    </template>

    <template #content>
      <v-col cols="12" v-for="day in days" :key="day">
        <v-card class="background-secondary rounded-lg" elevation="4">
          <v-card-item>

            <!-- activity card header -->
            <v-row class="justify-space-between align-center text-h6 pb-3" no-gutters>
              <span class="font-weight-bold">{{ formatDatePolish(day) }}</span>
              <AppButton
                  v-if="isOwnerValue"
                  color="primary-outline"
                  @click="showFormForDay = day"
                  v-show="showFormForDay !== day"
                  max-width="170px"
                  height-auto
                  font-auto
                  text="Dodaj aktywność"
              />
            </v-row>

            <!-- activity card body -->
            <ActivityForm
                v-if="showFormForDay === day"
                @submitActivity="(data) => addActivity(day, data)"
                @cancelForm="showFormForDay = null"
                class="mb-2"
            />

            <span v-if="!isSuccess">Ładuję...</span>

            <v-row v-else no-gutters>
              <ActivityCard
                  v-for="activityItem in activityByDate?.[day] ?? []"
                  :key="activityItem.id"
                  :activity="activityItem"
                  class="mb-3"
                  :isOwner="isOwnerValue"
              />
            </v-row>
          </v-card-item>
        </v-card>
      </v-col>
    </template>
  </Section>
</template>

<style scoped lang="scss">
.day-date {
  font-size: 1.2rem;
}
</style>
