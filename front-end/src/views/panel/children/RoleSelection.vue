<script setup lang="ts">
import {usePanelContentStore} from "@/stores/panelContentStore";
import RoleButton from "@/components/trip/RoleButton.vue";

const panelContentStore = usePanelContentStore();

const { roleSelection } = panelContentStore;
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
.role-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem auto;
  text-align: center;

  .title {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-color);
  }

  .subtitle {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 3.5rem;
    color: var(--text-color);
  }

  .roles-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 7rem;
  }

  @media (max-width: 800px) {
    .roles-container {
      gap: 2rem;
    }
    .title, .subtitle {
      font-size: 1.8rem;
    }
  }
}
</style>