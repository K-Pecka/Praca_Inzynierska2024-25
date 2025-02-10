<script lang="ts" setup>
interface Link{
    label:string,
    href: string,
}
defineProps({
  links: {
    type: Array as () => Link[],
    required: true
  },
})
</script>
<template>
    <div>
        <div v-for="link in links" :key="link.label">
        <a :href="link.href">{{ link.label }}</a>
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
</style>