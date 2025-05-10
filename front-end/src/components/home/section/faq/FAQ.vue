<script lang="ts" setup>
import { ref } from "vue";
import { FAQItem } from "@/types/interface";

const props = defineProps({
  faqList: {
    type: Array as () => FAQItem[],
    required: true,
  },
});

const openIndex = ref<number | null>(null);
const toggle = (index: number) => {
  openIndex.value = openIndex.value === index ? null : index;
};
</script>

<template>
  <div class="faq">
    <div class="faq__items"
      v-for="(item, index) in faqList"
      :key="index"
    >
      <div
        class="faq__item"
        :class="{ open: openIndex === index }"
        @click="toggle(index)"
      >
        <div class="faq__question">
          {{ item.question }}
          <span
            :class="{
              toggle__icon: true,
              'toggle__icon--open': openIndex === index,
            }"
          >+</span>
        </div>
        <div v-show="openIndex === index" class="faq__answer">
          {{ item.answer }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.faq {
  position: relative;
  width: 73%;
  .faq__items {
    .faq__item {
      transition: all 0.3s;
      border: 1px solid rgb(var(--v-theme-primary));
      width: 100%;
      padding: 1vw;
      margin: 1vw 0;
      border-radius: 0.5rem;
      background-color: rgb(var(--v-theme-secondary));
      cursor: pointer;
      .faq__question {
        color: rgb(var(--v-theme-primary));
        display: flex;
        justify-content: space-between;
        font-size: 15px;
        align-items: center;
        font-weight: bold;
        cursor: pointer;
      }

      .faq__answer {
        margin-top: 0.5rem;
        font-size: 15px;
        color: rgb(var(--v-theme-primary));
      }

      .toggle__icon {
        transition: all 0.3s;
        font-size: 1vw;
        line-height: 1;
        &--open {
          transform: rotate(45deg);
        }
      }
    }

    .faq__item.open .faq__question {
      color: var(--primary-color, #007bff);
    }
  }
}
</style>
