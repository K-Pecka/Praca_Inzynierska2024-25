<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {useActivityStore} from "@/stores/trip/useActivityStore";
import ActivityCard from "@/components/trip/module/activity/ActivityCard.vue";
import ActivityForm from "@/components/trip/module/activity/ActivityForm.vue";
import AppButton from "@/components/AppButton.vue";
import {Section} from "@/components";
import {useTripStore} from "@/stores/trip/useTripStore";
import {useRoute} from "vue-router";
import {Activity} from "@/types/interface";
import {useUtilsStore} from "@/stores/utils/useUtilsStore";

const {formatDatePolish} = useUtilsStore();
const route = useRoute();
const id = route.params.tripId as string;
const planId = route.params.planId as string;

const {data: activities, isSuccess} = useActivityStore().getActivity(
    id,
    planId
);

const {getPlans} = useTripStore();
const {data: plansData, isLoading, error} = getPlans(id);

function getDaysArray(start: Date, end: Date) {
  const arr = [];
  const dt = new Date(start);
  while (dt <= end) {
    const iso = dt.toISOString().split("T")[0];
    arr.push(iso);
    dt.setDate(dt.getDate() + 1);
  }
  return arr;
}

const days = computed(() => {
  if (plansData.value) {
    const plan = plansData.value.find((plan) => plan.id == Number(planId));
    if (plan) {
      return plan.start_date && plan.end_date
          ? getDaysArray(new Date(plan.start_date), new Date(plan.end_date))
          : null;
    }
  }
  return null;
});

const activityStore = useActivityStore();

const showFormForDay = ref<string | null>(null);

function addActivity(day: string, activityData: any) {
  //console.warn("send")
  activityStore.addActivity(
      {
        ...activityData,
        date: day,
      },
      {
        tripId: id,
        planId: planId,
      }
  );
}

import HeaderSection from "@/components/common/HeaderSection.vue";

const activity = computed(
    () =>
        activities.value &&
        activities.value.reduce((acc, activity) => {
          activity = {
            ...activity,
            date: activity.date || days?.value?.[0] || ""
          };
          if (!acc[activity.date]) {
            acc[activity.date] = [];
          }
          acc[activity.date].push(activity);
          //console.log(acc)
          return acc;
        }, {} as Record<string, Activity[]>)
)
onMounted(() => {
  activityStore.loadActivityTypes(id);
});

activityStore.loadActivityTypes(id);
</script>

<template>
  <Section>
    <template #title>
      <HeaderSection subtitle="Zarządzaj aktywnościami"/>
    </template>

    <template #content>
      <v-col cols="12" v-for="day in days" :key="day">
        <v-card class="background-secondary rounded-lg" elevation="4">
          <v-container>
            <v-card-item>

              <!-- Header with date and button -->
              <v-row class="justify-space-between align-center text-h6 pb-3" no-gutters>
                <div class="font-weight-bold">{{ formatDatePolish(day) }}</div>
                <AppButton
                    color="primary"
                    @click="showFormForDay = day"
                    v-show="showFormForDay != day"
                    height-auto
                    font-auto
                    text="Dodaj aktywność"
                />
              </v-row>

              <!-- Activity Form -->
              <ActivityForm
                  v-if="showFormForDay === day"
                  @submitActivity="(data) => addActivity(day, data)"
                  @cancelForm="showFormForDay = null"
                  class="mb-2"
              />

              <span v-if="!isSuccess">Ładuję...</span>

              <!-- Activity Cards -->
              <v-row v-else no-gutters>
                <ActivityCard
                    v-for="activityItem in activity?.[day] ?? []"
                    :key="activityItem.id"
                    :activity="activityItem"
                    class="mb-3"
                />
              </v-row>
            </v-card-item>
          </v-container>
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
