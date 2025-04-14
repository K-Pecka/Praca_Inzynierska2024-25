<script setup lang="ts">
import {Button, Trip} from "@/type/interface";

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
</script>

<template>
  <v-container  fluid class="full-width-container">
    <v-row>
      <v-col v-for="trip in props.trip" :key="trip.id" cols="12" sm="12" md="12" lg="6">
        <v-card>
          <v-row>
            <v-col cols="12" sm="6">
              <v-img :src="image" aspect-ratio="1.5" contain></v-img>
            </v-col>
            <v-col cols="12" sm="6" >
              <div class="trip-detail">
                <v-card-title>
                  {{ trip.name }}
                </v-card-title>
                <v-card-subtitle>
                  {{ formatPL(trip.start_date) }} - {{ formatPL(trip.end_date) }}
                </v-card-subtitle>
                <div class="detail">
                  <div
                    v-for="(button, index) in props.btn"
                    :key="index"
                    :className="button.class"
                  >
                    <v-btn @click="button.onclick(String(trip.id))">
                      {{ button.title }}
                    </v-btn>
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
.v-row{
  align-items: center;
}
.v-card-title {
  font-size: 1.5rem;
  font-family: var(--v-fontFamily);
  font-weight: bold;
}
.v-card-subtitle {
  font-size: 1rem;
  font-family: var(--v-fontFamily);
  font-weight: bold;
}
.trip-detail {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
@media (min-width: 600px) {
  .v-btn {
  font-size: 0.55rem;
  }
  .v-card-subtitle {
    font-size: 0.75rem;
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
