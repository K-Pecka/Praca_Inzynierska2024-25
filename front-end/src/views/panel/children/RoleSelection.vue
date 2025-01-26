<script setup lang="ts">
import {panelContentStore} from "@/stores/panelContentStore";
import RoleButton from "@/components/trip/RoleButton.vue";

const {roleSelection} = panelContentStore;

</script>

<template>
  <div class="role-selection">
    <h1 class="title">{{ roleSelection.title }}</h1>
    <p class="subtitle">{{ roleSelection.subtitle }}</p>
    <div class="roles-container">
      <RoleButton
          v-for="role in roleSelection.roles"
          :key="role.title"
          :title="role.title"
          :description="role.description"
          :image="role.image"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;

.role-selection {
  text-align: center;
  margin-top: 20px;

  h2 {
    font-size: 1.5rem;
    color: var(--text-color);
  }

  .roles {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1.5rem;

    .role-card {
      background-color: var(--secondary-color);
      border-radius: var(--secondary-color);
      padding: 1rem;
      width: 240px;
      text-align: center;
      box-shadow: var(--text-color);
      transition: transform 0.3s;

      &:hover {
        transform: scale(1.05);
      }

      .role-icon {
        height: 64px;
        margin-bottom: 1rem;
      }

      h3 {
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
        color: var(--text-color);
      }

      p {
        font-size: 0.875rem;
        color: var(--text-color);
      }
    }
  }
}
</style>