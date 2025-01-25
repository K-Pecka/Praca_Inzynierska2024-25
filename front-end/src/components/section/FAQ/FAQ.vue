<template>
  <div class="faq">
    <div class="faq-items">
      <div
        v-for="(item, index) in faqList"
        :key="index"
        class="faq-item"
        :class="{ open: openIndex === index }"
        @click="toggle(index)"
      >
        <div class="faq-question">
          <slot name="question" :question="item.question">{{
            item.question
          }}</slot>
          <span class="toggle-icon">{{ openIndex === index ? "-" : "+" }}</span>
        </div>
        <div v-if="openIndex === index" class="faq-answer">
          <slot name="answer" :answer="item.answer">{{ item.answer }}</slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, PropType } from "vue";

interface FAQItem {
  question: string;
  answer: string;
}

const props = defineProps({
  faqList: {
    type: Array as PropType<FAQItem[]>,
    required: true,
  },
});

const openIndex = ref<number | null>(null);

const toggle = (index: number) => {
  openIndex.value = openIndex.value === index ? null : index;
};
</script>

<style scoped lang="scss">
.faq {
  padding: 2rem 0;
  .faq-items {
    .faq-item {
      border: 1px solid var(--primary-color);
      width: 100%;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 0.5rem;
      background-color: var(--secondary-color);
      cursor: pointer;
      .faq-question {
        color: var(--primary-color);
        transition: all 0.3s;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        cursor: pointer;
      }

      .faq-answer {
        margin-top: 0.5rem;
        color: var(--primary-color);
      }

      .toggle-icon {
        font-size: 1.5rem;
        line-height: 1;
      }
    }

    .faq-item.open .faq-question {
      color: var(--primary-color, #007bff);
    }
  }
}
</style>
