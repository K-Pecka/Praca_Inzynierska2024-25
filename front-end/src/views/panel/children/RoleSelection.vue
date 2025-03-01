<script setup lang="ts">
import {usePagePanelStore} from "@/stores/ui/usePagePanelStore";
import RoleButton from "@/components/trip/RoleButton.vue";

const pagePanelStore = usePagePanelStore();
const getRoleSelection = pagePanelStore.getRoleSelection;

</script>

<template>
  <div class="role-selection">
    <h1 class="title">{{ getRoleSelection.title }}</h1>
    <p class="subtitle">{{ getRoleSelection.subtitle }}</p>
    <div class="roles-container">
      <RoleButton
          v-for="(role,index) in getRoleSelection.roles"
          :key="index"
          :role = "role"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.role-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  .title {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: rgb(var(--v-theme-text));
  }

  .subtitle {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 3.5rem;
    color: rgb(var(--v-theme-text));
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