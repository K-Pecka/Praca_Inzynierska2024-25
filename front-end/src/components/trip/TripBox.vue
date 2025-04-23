<script setup lang="ts">
import {Button, Trip} from "@/types/interface";

function formatPL(dateString: string): string {
  const dateObj = new Date(dateString);
  if (isNaN(dateObj.getTime())) return dateString;
  return new Intl.DateTimeFormat('pl-PL').format(dateObj);
}

const props = defineProps({
  btn: {
    type: Array as () => Button[],
    required: false,
  },
  trip: {
    type: Array as () => Trip[],
    required: true,
    default: () => []
  },
  image:{
    type: String,
  }
});
console.log(props);
</script>

<template>
  <v-container  fluid class="full-width-container">
    <v-row class="d-flex" style="justify-content: space-between">
      <v-col
        v-for="(trip, index) in props.trip"
        :key="trip.id"
        cols="12"
        sm="12"
        md="12"
        lg="6"
        class="d-flex"
        :class="index % 2 === 0 ? 'jusify-start' : 'justify-end'"
        :style="index % 2 === 0 ? 'padding-left: 0; padding-right: 4px;' : 'padding-right: 0; padding-left: 4px;'"
      >
        <v-card style="border-radius: 15px;padding-bottom:0.5rem;width: 100%;">
          <v-row style="height: 100%">
            <v-col cols="12" sm="4" style="height: 100%; width: 20rem; padding-right: 0px;">
              <img :src="image" style="height:100%;width:100%;" class="pl-2"/>
            </v-col>
            <v-col cols="12" sm="8" class="d-center">
              <div style="max-width:80%">
                <div class="trip-detail">
                  <div style="margin-bottom: .55rem;" class="d-center">
                    <v-card-title>
                  {{ trip.name }}
                </v-card-title>
                <v-card-subtitle>
                  {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }}
                </v-card-subtitle>
                  </div>
                
                <div class="detail">
                  <div
                    v-for="(button, index) in props.btn"
                    :key="index"
                    :className="button.class"
                  >
                    <v-btn @click="button.onclick(String(trip.id))" style="border-radius: 15px; text-transform: none;">
                      {{ button.title }}
                    </v-btn>
                  </div>
                </div>
              </div>
              </div>
              
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
.d-center{
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
.v-card{
  background-color: rgba(var(--v-theme-secondary),50%);
}
.v-card--variant-elevated {
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.v-row{
  align-items: center;
}
.v-card-title {
  font-size: 1.25rem;
  font-family: var(--v-fontFamily);
  color:rgba(var(--v-theme-text),100%);
  font-weight: bold;
  padding-bottom: 0.3rem;
}
.v-card-subtitle {
  color:rgba(var(--v-theme-text),100%);
  font-family: var(--v-fontFamily);
  font-weight: bold;
  padding-bottom: 0.6rem;
}
.trip-detail {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
@media (min-width: 600px) {
  .v-btn {
    font-size: 0.75rem;
  }
  .v-card-subtitle {
    font-size: 0.9rem;
  }
}
.v-btn {
  margin:auto;
  margin-top: 0.6rem;
  min-width: 100%;
}
.detail{
  width: 90%;
}
.primary button {
  background-color: rgb(var(--v-theme-primary));
}
.accent button {
  background-color: rgb(var(--v-theme-accent));
}
button {
  color: #eee;
  margin: 0 1rem;
}
</style>

