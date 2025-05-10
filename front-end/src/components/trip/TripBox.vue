<script setup lang="ts">
import {Button, Trip, Image} from "@/types/interface";

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
    type: Object as () => Image,
  }
});
</script>

<template>

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
  color:rgba(var(--v-theme-text),100%);
  font-weight: bold;
  padding-bottom: 0.3rem;
}
.v-card-subtitle {
  color:rgba(var(--v-theme-text),100%);
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

