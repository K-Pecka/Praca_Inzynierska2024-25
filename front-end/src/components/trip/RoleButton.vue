<script setup lang="ts">
import {Role} from "@/types/interface";
import { PropType } from "vue";

const props = defineProps({
  role: {
    type: Object as PropType<Role>,
    required: true,
  },
});


</script>

<template>
  <router-link :to="role.path" style="display: flex; justify-content: center;">
    <button class="role-button">
      <img :src="role.image" alt="" class="role-icon" />
      <h2 class="role-title">{{ role.title }}</h2>
      <p class="role-description">{{ role.description }}</p>
    </button>
  </router-link>
  
</template>

<style scoped lang="scss">
.role-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 15px;
  padding: 2.5rem 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  width: 33rem;

  @media (max-width: 480px) {
    width: 20rem;
  }
  @media (max-width: 360px) {
    width: 18rem;
  }

  &:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.35);
  }

  .role-icon {
    width: 153px;
    height: 153px;
    margin-bottom: 1rem;

    @media (max-width: 480px) {
      width: 90px;
      height: 90px;
    }
  }

  .role-title {
    font-size: 38px;
    color: rgb(var(--v-theme-text));

    @media (max-width: 480px) {
      font-size: 1.4rem;
    }
  }

  .role-description {
    font-size: 18px;
    font-weight: 700;
    color: rgb(var(--v-theme-text));
    line-height: 1.1;
    text-align: center;
  }
}
</style>