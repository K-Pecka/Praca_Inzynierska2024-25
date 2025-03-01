<template>
  <section class="section">
    <header class="section__header">
      <slot name="title"></slot>
    </header>
    <div class="section__content">
      <slot name="content"></slot>
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;
.section {
  @include section-width;
  margin: 1rem 5rem 2rem;
  &__header {
    text-align: center;
    font-size: 1.5rem;
    margin: 2rem 0;
    color: var(--v-theme-text, #333);
  }

  &__content {
    font-size: 1rem;
    line-height: 1.5;
    color: var(--v-theme-text, #666);
    width: 100%;
  }
}
</style>
