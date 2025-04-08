<script setup lang="ts">
import { computed, ref } from "vue";
import { useActivityStore } from "@/stores/trip/useActivityStore";
import ActivityList from "@/components/trip/modul/activity/ActivityList.vue";
import ActivityForm from "@/components/trip/modul/activity/ActivityForm.vue";
import AppButton from "@/components/budget/AppButton.vue";
import {Section} from "@/components";
import  {useTripStore} from "@/stores/trip/useTripStore";
import { useRoute } from "vue-router";
const route = useRoute();
const id = route.params.tripId as string;
const planId = route.params.planId as string;
const startDate = new Date("2025-04-15");
const endDate = new Date("2025-04-24");
const { getPlans } = useTripStore();
const { data: plansData, isLoading, error } = getPlans(id);
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
  activityStore.addActivity({
    ...activityData,
    date: day,
  },{
    tripId: id,
    planId: planId,
  });
  showFormForDay.value = null;
}
import HeaderSection from "@/components/common/HeaderSection.vue";
</script>

<template>
  <div class="page-container">
    <Section>
      <template #title>
        <HeaderSection>
              <template #subtitle>
                 <h2 class="trip-title">Zarządzaj aktywnościami</h2>
              </template>
              </HeaderSection>
      </template>

      <template #content>
        <div
            v-for="day in days"
            :key="day"
            class="day-card"
        >
          <div class="day-card-header">
            <div class="day-date">{{ day }}</div>
            <AppButton variant="primary" size="sm" @click="showFormForDay = day">
              Dodaj aktywność
            </AppButton>
          </div>

          <ActivityForm
              v-if="showFormForDay === day"
              @submitActivity="(data) => addActivity(day, data)"
              @cancelForm="showFormForDay = null"
              class="form-container"
          />

          <ActivityList :activities="activityStore.activitiesByDate(day).value" />
        </div>
      </template>
    </Section>
  </div>
</template>

<style scoped lang="scss">
.page-container {
  max-width: 88rem;
  margin: 0 auto;
}

.header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.title-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.trip-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 0.2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 500;
  margin: 0;
}

.day-card {
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 1rem;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.15);
}

.day-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.day-date {
  font-weight: 600;
  font-size: 1.1rem;
}

.form-container {
  margin-bottom: 1rem;
}
</style>