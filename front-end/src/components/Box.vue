<script lang="ts" setup>
import { ref, onMounted} from 'vue';

interface Box {
  title: string;
  content: string | string[];
  set: {
    size: {
      sm?: { col: number, row: number };
      md?: { col: number, row: number };
      lg?: { col: number, row: number };
      xl?: { col: number, row: number };
    };
    order: number;
  };
}

const props = defineProps<Box>();

const screenWidth = ref(window.innerWidth);
const screenBreakpoint = ref('');

const breakpoints = {
  xs: 0,
  sm: 600,
  md: 960,
  lg: 1280,
  xl: 1920,
};

const checkBreakpoint = () => {
  if (screenWidth.value < breakpoints.sm) {
    screenBreakpoint.value = 'xs';
  } else if (screenWidth.value < breakpoints.md) {
    screenBreakpoint.value = 'sm';
  } else if (screenWidth.value < breakpoints.lg) {
    screenBreakpoint.value = 'md';
  } else if (screenWidth.value < breakpoints.xl) {
    screenBreakpoint.value = 'lg';
  } else {
    screenBreakpoint.value = 'xl';
  }
};

onMounted(() => {
  window.addEventListener('resize', () => {
    screenWidth.value = window.innerWidth;
    checkBreakpoint();
  });
  checkBreakpoint();
});

const getGridCols = () => {
  const { size } = props.set;
  const breakpoint = screenBreakpoint.value;

  switch (breakpoint) {
    case 'xs':
      return size?.sm?.col || 12;
    case 'sm':
      return size?.sm?.col || size?.md?.col || 12;
    case 'md':
      return size?.md?.col || size?.lg?.col || 12;
    case 'lg':
      return size?.lg?.col || size?.md?.col || 12;
    case 'xl':
      return size?.xl?.col || size?.lg?.col || 12;
    default:
      return 12;
  }
};

const getGridRows = () => {
  const { size } = props.set;
  const breakpoint = screenBreakpoint.value;

  switch (breakpoint) {
    case 'xs':
      return size?.sm?.row || 1;
    case 'sm':
      return size?.sm?.row || size?.md?.row || 1;
    case 'md':
      return size?.md?.row || size?.lg?.row || 1;
    case 'lg':
      return size?.lg?.row || size?.md?.row || 1;
    case 'xl':
      return size?.xl?.row || size?.lg?.row || 1;
    default:
      return 1;
  }
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
        <v-list>
          <v-list-item v-for="(item, index) in props.content" :key="index">
            <v-list-item-content>
              {{ item }}
            </v-list-item-content>
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
  height: 100%;
}
.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}
</style>
