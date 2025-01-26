<template>
  <section class="section">
    <header class="section-header">
      <slot name="title"></slot>
    </header>
    <div class="section-content">
      <slot name="content"></slot>
    </div>
  </section>
</template>

<script lang="ts" setup>
const props = defineProps({
  customClass: {
    type: String,
    default: "",
  },
});
</script>

<style scoped lang="scss">
@use "@/assets/style" as *;
.section {
  @include section-width;
  padding: 2rem 0.5rem;
  border-radius: 0.5rem;
  &-header {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text-color, #333);
  }

  &-content {
    font-size: 1rem;
    line-height: 1.5;
    color: var(--text-color, #666);
    width: 100%;
  }
}
</style>
