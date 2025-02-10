<script lang="ts" setup>
interface SubSectionItem {
  image: string;
  alt: string;
  caption: string;
}

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

  &__title {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  &__content {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  &__item {
    text-align: center;
    width: 14rem;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    padding: 1rem;
  }

  &__imageContainer {
    width: 100%;
    height: 13rem;
    margin-bottom: 0.5rem;

    &-colorBox {
      width: 100%;
      min-height: 12rem;
      background-color: rgba(47, 39, 206, 0.3);
      border-radius: 15px;
    }
  }
  &__caption {
    font-size: 1rem;
    color: rgb(var(--v-theme-text));
    letter-spacing: 2px;
    font-weight: 700;
    font-family: var(--v-fontFamily);
  }
}
</style>
