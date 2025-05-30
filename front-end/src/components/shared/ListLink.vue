<script lang="ts" setup>
  import { Link } from "@/types/interface";

  defineProps({
    links: {
      type: Array as () => Link[],
      required: true
    },
  })
</script>
<template>
  <div class="list-link">
    <div v-for="link in links" :key="link.label">
      <router-link :to="link.href">{{ link.label }}</router-link>
    </div>
  </div>
    
</template>
<style lang="scss" scoped>
 div > div:not(:first-child){
    margin-top: 2rem;
  }
  a{
    color:rgb(var(--v-theme-text));
  }
  .list-link {
    display: flex;
    flex-direction: column;
    margin: 0rem;
  }
</style>