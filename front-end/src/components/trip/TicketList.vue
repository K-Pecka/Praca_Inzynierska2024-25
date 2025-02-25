<script setup lang="ts">
import { defineProps } from "vue";
import TicketCard from "./TicketCard.vue";


const props = defineProps({
  tickets: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <div class="ticket-list">
    <TicketCard
        v-for="ticket in tickets"
        :key="ticket.id"
        :ticket="ticket"
    />
  </div>
</template>


<style scoped lang="scss">
.ticket-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
