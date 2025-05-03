<template>
  <v-container>
    <v-col cols="12" class="section mx-auto mt-5">
      <v-sheet elevation="0" class="section__header bg-transparent mb-10">
        <slot name="title"></slot>
      </v-sheet>
      <v-sheet elevation="0" class="section__content bg-transparent" >
        <slot name="content"></slot>
      </v-sheet>
      <v-sheet elevation="0" class="section__footer bg-transparent">
        <slot name="footer"></slot>
      </v-sheet>
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

  &__content {
    line-height: 1.5;
    color: $text-color;
    width: 100%;
  }
}

</style>
<script setup lang="ts">
</script>
