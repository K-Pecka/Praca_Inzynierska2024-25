<script setup lang="ts">
import { computed, ref } from "vue";
import { useActivityStore } from "@/stores/trip/useActivityStore";
import ActivityList from "@/components/trip/module/activity/ActivityList.vue";
import ActivityForm from "@/components/trip/module/activity/ActivityForm.vue";
import AppButton from "@/components/budget/AppButton.vue";
import { Section } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { useRoute } from "vue-router";
import { Activity } from "@/types/interface";
const route = useRoute();
const id = route.params.tripId as string;
const planId = route.params.planId as string;

const { data: activities, isSuccess } = useActivityStore().getActivity(
  id,
  planId
);

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
  console.warn("send")
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
      console.log(acc)
      return acc;
    }, {} as Record<string, Activity[]>)
  )
</script>

<template>
  <div class="page-container py-10">
    <Section>
      <template #title>
        <HeaderSection>
          <template #subtitle>
            <h2 class="trip-title mb-10" style="font-size: 30px; font-weight: 600; width: 80%;">Zarządzaj aktywnościami</h2>
          </template>
        </HeaderSection>
      </template>

      <template #content>
        <div v-for="day in days" :key="day" class="day-card w-100">
          <div class="day-card-header">
            <div class="day-date">{{ day }}</div>
            <AppButton
              variant="primary"
              size="sm"
              @click="showFormForDay = day"
              v-show="showFormForDay != day"
            >
              Dodaj aktywność
            </AppButton>
          </div>

          <ActivityForm
            v-if="showFormForDay === day"
            @submitActivity="(data) => addActivity(day, data)"
            @cancelForm="showFormForDay = null"
            class="form-container"
          />
          <span v-if="!isSuccess">Ładuję...</span>
          <ActivityList v-else :activities="activity?.[day] ?? []" />
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
