<script lang="ts" setup>
import { SubSectionItem } from "@/types";
defineProps({
  items: {
    type: Array as () => SubSectionItem[],
    required: true,
  },
});
</script>

<template>
  <div class="subSection">
    <h3 class="subSection__title">
      <slot name="title"></slot>
    </h3>
    <div class="subSection__content">
      <div
        class="subSection__item"
        v-for="(item, index) in items"
        :key="index"
      >
        <div class="subSection__imageContainer">
          <div class="subSection__imageContainer-colorBox">
            <img :src="item.image" :alt="item.alt" />
          </div>
        </div>
        <div class="subSection__caption">
          <p>{{ item.caption }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
img {
  width: 100%;
  height: 100%;
}
.subSection {
  margin: 5rem 0;
  width: 100%;

  &__title {
    font-size: 3vw;
    margin-bottom: clamp(0.5rem, 5vw, 1.5rem);
    text-align: center;
  }

  &__content {
    display: flex;
    width: auto;
    flex-wrap: wrap;
    justify-content: center;
  }

  &__item {
    text-align: center;
    width: clamp(20rem, 15vw, 150rem);
    margin-left: 1%;
    margin-right: 1%;
  }

  &__imageContainer {
    width: 100%;

    &-colorBox {
      width: 100%;
      background-color: rgba(var(--v-theme-secendar,47, 39, 206, 0.3));
      border-radius: 10%;
    }
  }
  &__caption {
    font-size: 1.2vw;
    color: rgb(var(--v-theme-text));
    letter-spacing: 2px;
    font-weight: 700;
    font-family: var(--v-fontFamily);
  }
}
</style>
