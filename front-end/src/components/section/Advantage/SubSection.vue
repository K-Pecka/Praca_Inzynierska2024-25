<template>
    <div class="sub-section">
      <h3 class="sub-section__title">
        <slot name="title"></slot>
      </h3>
      <div class="sub-section__content">
        <div class="sub-section__item" v-for="(item, index) in items" :key="index">
          <div class="sub-section__image-container">
            <div class="sub-section__color-box">
              <img :src="item.image" :alt="item.alt" />
            </div>
          </div>
          <div class="sub-section__caption">
            <p>{{ item.caption }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
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
  
  <style scoped lang="scss">
  img{
    width: 100%;
    height: 100%;
  }
  .sub-section {
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
  
    &__image-container {
      width: 100%;
      height: 13rem;
      margin-bottom: 0.5rem;
    }
  
    &__color-box {
      width: 100%;
      min-height: 12rem;
      background-color: rgba(47, 39, 206, 0.3);
      border-radius: 15px;
    }
  
    &__caption {
      font-size: 1rem;
      color: var(--text-color);
      letter-spacing: 2px;
      font-weight: 700;
      font-family: var(--font-family);
    }
  }
  </style>
  