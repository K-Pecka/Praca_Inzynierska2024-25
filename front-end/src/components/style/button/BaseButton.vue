<script setup lang="ts">
import { computed } from "vue";

interface ButtonProps {
  variant: "default" | "outlined" | "primary" | "secondary" | "danger";
  size: "small" | "medium" | "large";
}

const props = defineProps<ButtonProps>();

const buttonClass = computed(() => {
  let classes = ["v-btn"];

  switch (props.variant) {
    case "primary":
      classes.push("v-btn--primary");
      break;
    case "secondary":
      classes.push("v-btn--secondary");
      break;
    case "danger":
      classes.push("v-btn--danger");
      break;
    case "outlined":
      classes.push("v-btn--outlined");
      break;
    default:
      classes.push("v-btn--default");
      break;
  }
  if (props.size === "small") classes.push("v-btn--small");
  if (props.size === "large") classes.push("v-btn--large");

  return classes.join(" ");
});

const buttonStyle = computed(() => {
  if (props.variant === "primary") {
    return { backgroundColor: "#1976D2", color: "#fff" };
  }
  if (props.variant === "danger") {
    return { backgroundColor: "#E53935", color: "#fff" };
  }
  return {};
});


</script>

<template>
  <v-btn :class="buttonClass" :style="buttonStyle" @click="handleClick">
    <slot></slot>
  </v-btn>
</template>

<style scoped>
.v-btn {
  padding: 0.5rem 10rem;
  border-radius: 0.25rem;
}
</style>
