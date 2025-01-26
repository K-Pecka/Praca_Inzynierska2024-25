<script setup lang="ts">
import { defineProps } from "vue";

defineProps({
  title: String,
  description: String,
  image: String,
});


</script>

<template>
  <button class="role-button">
    <img :src="image" alt="" class="role-icon" />
    <h2 class="role-title">{{ title }}</h2>
    <p class="role-description">{{ description }}</p>
  </button>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;

.role-button {
  background-color: rgba(var(--secondary-color),0.5);
  border: 1px solid var(--secondary-color);
  border-radius: var(--border-radius);
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  width: 260px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .role-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 16px;
  }

  .role-title {
    @include font-large;
    font-size: 20px;
    margin-bottom: 8px;
  }

  .role-description {
    @include font-regular;
    font-size: 14px;
  }
}
</style>