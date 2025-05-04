<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";
import { DashboardBox } from "@/types/interface";

const props = defineProps<DashboardBox>();
const screenWidth = ref(window.innerWidth);
const screenBreakpoint = ref("");

const breakpoints = {
  xs: 0,
  sm: 600,
  md: 960,
  lg: 1280,
  xl: 1920,
};

const checkBreakpoint = () => {
  if (screenWidth.value < breakpoints.sm) {
    screenBreakpoint.value = "xs";
  } else if (screenWidth.value < breakpoints.md) {
    screenBreakpoint.value = "sm";
  } else if (screenWidth.value < breakpoints.lg) {
    screenBreakpoint.value = "md";
  } else if (screenWidth.value < breakpoints.xl) {
    screenBreakpoint.value = "lg";
  } else {
    screenBreakpoint.value = "xl";
  }
};

const handleResize = () => {
  screenWidth.value = window.innerWidth;
  checkBreakpoint();
};

onMounted(() => {
  window.addEventListener("resize", handleResize);
  checkBreakpoint();
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
});

const getGridCols = () => {
  const { size } = props.set;
  const breakpoint = screenBreakpoint.value as keyof typeof size;

  return size[breakpoint]?.col || size.lg?.col || 12;
};

const getGridRows = () => {
  const { size } = props.set;
  const breakpoint = screenBreakpoint.value as keyof typeof size;

  return size[breakpoint]?.row || size.lg?.row || 1;
};

import BudgetContent from "@/components/ui/BudgetContent.vue";
</script>

<template>
  <v-card
    class="px-5 pt-2 pb-3 rounded-lg"
    elevation="3"
    :style="{
      gridColumn: `span ${getGridCols()}`,
      gridRow: `span ${getGridRows()}`,
      order: props.set.order,
    }"
  >
    <v-card-title class="text-h6 font-weight-bold py-5 px-0 d-flex align-center">
      <v-icon class="mr-2" color="primary">{{ `${props.icon}` }}</v-icon>
      {{ props.title }}
    </v-card-title>
    <v-card-text class="px-0 py-0 text-h6 font-weight-bold">
      <template v-if="Array.isArray(props.content)">
        <v-list v-if="props.content.length > 0">
          <v-list-item v-for="(item, index) in props.content" :key="index">
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
      <template
        v-if="typeof props.content === 'object' && props.content !== null"
      >
        <BudgetContent
          v-if="
            typeof props.content === 'object' &&
            props.content !== null &&
            !Array.isArray(props.content)
          "
          :content="props.content"
        />
      </template>
      <template v-else>
        <span :class="props.className"
          >{{ props.content }} {{ props.className }}</span
        >
      </template>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;

.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: $background-secondary;
}
.v-card-title {
  color: $text-color;
}

.v-card:hover {
  transform: translateY(-3px);
}
</style>
