<script setup lang="ts">
import TicketCard from "./TicketCard.vue";
import { Ticket} from "@/type";

const props = defineProps({
  tickets: {
    type: Array as () => Ticket[],
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
