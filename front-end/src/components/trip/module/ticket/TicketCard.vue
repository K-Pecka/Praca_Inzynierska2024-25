<script setup lang="ts">
import { TicketData } from "@/types";

defineProps({
  ticket: {
    type: Object as () => TicketData,
    required: true,
  },
});

</script>

<template>

</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;



.ticket-icon {
  color: $text-color;
}
</style>
