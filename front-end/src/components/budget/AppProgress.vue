<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ value: number; max: number }>();
const percentage = computed(() => (props.value / props.max) * 100);
</script>

<template>
  <div class="progress-bar">
    <div class="progress" :style="{ width: percentage + '%' }"></div>
  </div>
</template>

<style scoped>
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #4caf50;
  transition: width 0.3s ease-in-out;
}
</style>
