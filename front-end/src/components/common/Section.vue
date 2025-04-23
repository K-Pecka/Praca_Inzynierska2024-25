<template>
  <section class="section">
    <header class="section__header">
      <slot name="title"></slot>
    </header>
    <div class="section__content">
      <slot name="content"></slot>
    </div>
    <div class="section__footer">
      <slot name="footer"></slot>
    </div>
  </section>
</template>

<style scoped lang="scss">
@use "@/assets/style" as *;
.section {
  @include section-width;
  margin: 1rem 5rem 2rem;
  @media (max-width: 600px) {
    margin: 1rem 0.5rem 2rem;
  }
  @media (min-width: 600px) and (max-width: 800px) {
    margin: 1rem 3rem 2rem;
  }
  @media (min-width: 800px) and (max-width: 1200px) {
    margin: 1rem 4rem 2rem;
  }
  &__header {
    text-align: center;
    font-size: 2rem;
    margin: 1rem 0 0.1rem 0;
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
