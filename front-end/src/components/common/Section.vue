<template>
  <v-container>
    <div class="section mx-auto mt-10">
      <header class="section__header">
        <slot name="title"></slot>
      </header>
      <div class="section__content" >
        <slot name="content"></slot>
      </div>
      <div class="section__footer">
        <slot name="footer"></slot>
      </div>
    </div>

  </v-container>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables" as *;
@use "@/assets/styles/style" as *;

.section__content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.section {
  width: $panel-content-width;

  &__header {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: $panel-header-font-size;
    color: $text-color;
  }

  &__content {
    font-size: 1rem;
    line-height: 1.5;
    color: var(--v-theme-text, #666);
    width: 100%;
  }
}
</style>
<script setup lang="ts">
</script>
