<script setup lang="ts">
defineProps({
  cols: {
    type: String,
    default: '10',
    required: false,
  },
});
</script>

<template>
  <v-container>
    <v-col cols="12" class="section">
      <v-row elevation="0" class="section__header bg-transparent mb-10 align-content-space-around" justify="center">
        <v-col :cols="12" :sm="cols" :md="cols" :lg="cols">
          <slot name="title"></slot>
        </v-col>
      </v-row>
      <v-row elevation="0" class="section__content bg-transparent" justify="center">
        <v-col :cols="12" :sm="cols" :md="cols" :lg="cols">
          <slot name="content"></slot>
        </v-col>
      </v-row>
      <v-col :cols="12" :sm="cols" :md="cols" :lg="cols">
        <v-row elevation="0" class="section__footer bg-transparent">
          <slot name="footer"></slot>
        </v-row>
      </v-col>
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
  }

  &__content {
    line-height: 1.5;
    color: $text-color;
  }
}

</style>
