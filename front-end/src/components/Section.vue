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
  margin: 5rem 0;
  &__header {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text-color, #333);
  }

  &__content {
    font-size: 1rem;
    line-height: 1.5;
    color: var(--text-color, #666);
    width: 100%;
  }
}
</style>
