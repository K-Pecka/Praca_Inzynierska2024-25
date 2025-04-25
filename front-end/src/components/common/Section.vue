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
@use "@/assets/styles/style" as *;
.section__content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.section {
  &__header {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
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
