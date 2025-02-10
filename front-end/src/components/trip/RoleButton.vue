<script setup lang="ts">


const props = defineProps({
  title: String,
  description: String,
  image: String,
  path: {type: String,default: '/'}
});


</script>

<template>
  <router-link :to="path">
    <button class="role-button">
      <img :src="image" alt="" class="role-icon" />
      <h2 class="role-title">{{ title }}</h2>
      <p class="role-description">{{ description }}</p>
    </button>
  </router-link>
  
</template>

<style scoped lang="scss">
.role-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border: none;
  border-radius: 15px;
  padding: 2rem 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-width: 15rem;
  max-width: 25rem;
  flex: 1 1 auto;

  &:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.35);
  }

  .role-icon {
    width: 153px;
    height: 153px;
    margin-bottom: 1rem;
    object-fit: contain;
  }

  .role-title {
    font-size: 1.9rem;
    color: rgb(var(--v-theme-text));
    margin-bottom: 0.5rem;
  }

  .role-description {
    font-size: 1rem;
    color: rgb(var(--v-theme-text));
    line-height: 1.5;
    text-align: center;
  }
}
</style>