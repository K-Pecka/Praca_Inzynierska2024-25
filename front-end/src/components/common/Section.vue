<template>
  <v-container>
    <v-col cols="12" class="section mx-auto mt-5">
      <header class="section__header">
        <slot name="title"></slot>
      </header>
      <div class="section__content" >
        <slot name="content"></slot>
      </div>
      <div class="section__footer">
        <slot name="footer"></slot>
      </div>
    </v-col>

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
    font-size: 2rem;
    line-height: 1.5;
    color: $text-color;
    width: 100%;
  }
}
</style>
<script setup lang="ts">
</script>
