<script lang="ts" setup>
import { ref } from "vue";
interface FAQItem {
  question: string;
  answer: string;
}

const props = defineProps({
  faqList: {
    type:  Array as () => FAQItem[],
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
    <div class="faq__items">
      <div
        v-for="(item, index) in faqList"
        :key="index"
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
            >+</span
          >
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
  padding: 2rem 0;
  .faq__items {
    .faq__item {
      transition: all 0.3s;
      border: 1px solid var(--primary-color);
      width: 100%;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 0.5rem;
      background-color: var(--secondary-color);
      cursor: pointer;
      .faq__question {
        color: var(--primary-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        cursor: pointer;
      }

      .faq__answer {
        margin-top: 0.5rem;
        color: var(--primary-color);
      }

      .toggle__icon {
        transition: all 0.3s;
        font-size: 1.5rem;
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
