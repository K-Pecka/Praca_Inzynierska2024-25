<script setup lang="ts">
import TicketCard from "./TicketCard.vue";
import { TicketData } from "@/types";
import { useRoute } from "vue-router";
const props = defineProps({
  tickets: {
    type: Array as () => TicketData[],
    default: () => [],
  },
});
const route = useRoute();
const id = route.params.tripId as string;
const getTicket = () => {
  return (
    props.tickets.filter((ticket) => ticket.trip === Number(id)) ??
    ([] as TicketData[])
  );
};
console.log("Tickets", props.tickets);
</script>

<template>
  <div class="ticket-list">
    <template v-if="[...getTicket()]?.length !== 0">
      <TicketCard
        v-for="ticket in getTicket().reverse()"
        :key="ticket.id"
        :ticket="ticket"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.ticket-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
