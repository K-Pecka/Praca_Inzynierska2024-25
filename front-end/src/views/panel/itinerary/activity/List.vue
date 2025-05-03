<script setup lang="ts">
import { computed, ref } from "vue";
import { useActivityStore } from "@/stores/trip/useActivityStore";
import ActivityCard from "@/components/trip/module/activity/ActivityCard.vue";
import ActivityForm from "@/components/trip/module/activity/ActivityForm.vue";
import AppButton from "@/components/budget/AppButton.vue";
import { Section } from "@/components";
import { useTripStore } from "@/stores/trip/useTripStore";
import { useRoute } from "vue-router";
import { Activity } from "@/types/interface";
import {useUtilsStore} from "@/stores/utils/useUtilsStore";

const { formatDatePolish } = useUtilsStore();
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
  <Section>
    <template #title>
      <HeaderSection subtitle="Zarządzaj aktywnościami" />
    </template>

    <template #content>
      <div v-for="day in days" :key="day" class="day-card w-100">
        <div class="day-card-header">
          <div class="day-date">{{ formatDatePolish(day) }}</div>
          <AppButton
            variant="primary"
            @click="showFormForDay = day"
            v-show="showFormForDay != day"
            text="Dodaj aktywność"
          />
        </div>

        <ActivityForm
          v-if="showFormForDay === day"
          @submitActivity="(data) => addActivity(day, data)"
          @cancelForm="showFormForDay = null"
          class="form-container"
        />
        <span v-if="!isSuccess">Ładuję...</span>
        <div class="activity-list" v-else>
          <ActivityCard
              v-for="activityItem in activity?.[day] ?? []"
              :key="activityItem.id"
              :activity="activityItem"
          />
        </div>
      </div>
    </template>
  </Section>
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
  padding: 25px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.15);
}

.day-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: .5rem;

  @media (max-width: 480px) {
    flex-direction: column;
    align-items: flex-start;

    button {
      width: 100%;
    }
  }
}

.day-date {
  font-weight: 600;
  font-size: 1.2rem;
}

.form-container {
  margin-bottom: 1rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
