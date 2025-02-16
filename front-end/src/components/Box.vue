<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";

interface Box {
  title: string;
  content: string | string[];
  set: {
    size: {
      sm?: { col: number; row: number };
      md?: { col: number; row: number };
      lg?: { col: number; row: number };
      xl?: { col: number; row: number };
    };
    order: number;
  };
}

const props = defineProps<Box>();

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
</script>

<template>
  <v-card
    class="pa-4 rounded-lg"
    elevation="3"
    :style="{
      gridColumn: `span ${getGridCols()}`,
      gridRow: `span ${getGridRows()}`,
      order: props.set.order,
    }"
  >
    <v-card-title class="text-h6 font-weight-medium">
      {{ props.title }}
    </v-card-title>
    <v-card-text>
      <template v-if="Array.isArray(props.content)">
        <v-list v-if="props.content.length > 0">
          <v-list-item v-for="(item, index) in props.content" :key="index">
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
      <template v-else>
        {{ props.content }}
      </template>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: rgb(var(--v-theme-secondary), 50%);
  height: 100%;
  border-radius: 1.5rem;
}
.v-card-title {
  font-size: 20px;
  font-weight: bold;
  font-family: var(--v-fontFamily);
  padding-bottom: 2rem;
}
.v-card-text {
  font-size: 20px;
  font-family: var(--v-fontFamily);
}
.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>
