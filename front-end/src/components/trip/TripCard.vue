<script setup lang="ts">

function formatPL(dateString: string): string {
  const dateObj = new Date(dateString);
  if (isNaN(dateObj.getTime())) return dateString;
  return new Intl.DateTimeFormat('pl-PL').format(dateObj);
}

const props = defineProps<{
  plans: any;
  btn: any;
}>();
console.log('plany:', props.plans)
console.log('plany:', props.plans.length)
console.log(props.plans.activities_count)
</script>

<template>
  <v-container fluid class="trip-container px-0">
    <v-row v-if="props.plans.length > 0">
      <v-col
        v-for="(trip, index) in plans"
        :key="index"
        cols="12"
        sm="12"
        md="12"
        lg="12"
        class="px-0"
      >
        <v-card class="trip-card pa-5" elevation="3">
          <v-row>
            <v-col cols="6">
              <v-card-title class="text-h6 font-weight-bold py-0">
                {{ trip.name }}
              </v-card-title>
              <v-card-subtitle class="px-0 pb-1 font-weight-medium">
                {{ trip.country }} {{ trip?.description ?? "brak opisu" }}
              </v-card-subtitle>
              <v-card-text class="px-0 py-0 font-weight-medium">
                {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }} <span class="activity-number ml-2">{{trip.activities_count || 0}} aktywności</span>
              </v-card-text>
            </v-col>
            <v-col cols="6" class="d-flex flex-row justify-end align-center">
              <v-btn
                v-for="(action, i) in btn"
                :key="i"
                @click="action.onclick(String(trip.trip),String(trip.id))"
                variant="flat"
                :style="{'min-width': 'auto', 'background-color': 'transparent'}"
                class="px-2"
                
              >
                <v-icon style="width: 30px; height: 30px;" contain :color="action.class">
                  {{ action.icon }}
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
.activity-number {
  color: rgb(var(--v-theme-accent), 0.75);
}
.trip-container {
  padding: 16px;
}
.trip-card {
  border-radius: 16px;
  background-color: rgba(var(--v-theme-secondary), 0.5);
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}
.v-card-actions {
  margin-top: 3rem;
}
.v-card-title {
  font-family: var(--v-FontFamily);
}
@media (max-width: 600px) {
.v-card-actions {
  flex-direction: column;
}
}
@media (min-width: 600px) {
  .v-card-actions {
  flex-direction: row;
}
}
</style>
