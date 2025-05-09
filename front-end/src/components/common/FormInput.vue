<template>
  <div class="input-wrapper">
    <label
      :for="inputData.name"
      class="input-label"
      :class="{ required: inputData.config?.required }"
      >{{ inputData.label }}</label
    >

    <template v-if="inputData.type === 'date_range'">
      <v-date-input
        :min="inputData.config?.min"
        :max="inputData.config?.edit ?? inputData.config?.max"
        v-model="localRange"
        :label="inputData.config?.edit ? `${inputData.config?.min} - ${inputData.config?.max}` : inputData.placeholder"
        :multiple="inputData.config?.multiple ? 'range' : false"
        :placeholder="inputData.placeholder"
        max-width="auto"
        variant="outlined"
        prepend-icon=""
        prepend-inner-icon="mdi-calendar"
        bg-color="background"
        @update:modelValue="onRangeChange"
        color="primary"
        :clearable="true"
        header-color="primary"
      />
    </template>

    <template v-else>
      <input
        :name="inputData.name"
        :id="inputData.name"
        :type="inputData.type"
        :placeholder="inputData.placeholder"
        @input="updateModel"
        @blur="handleInput"
        class="input background"
        :class="{ error: inputData.error && inputData.error.length > 0 }"
      />
    </template>

    <div>
      <span
        v-for="(error, index) in inputData.error"
        :key="index"
        class="showError"
        >{{ error }}</span
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { VDateInput } from "vuetify/labs/components";
import { Input } from "@/types/interface";

const props = defineProps({
  inputData: {
    type: Object as () => Input,
    required: true,
  },
  modelValue: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(["update", "updateModel"]);

const localRange = ref<string[]>(
  Array.isArray(props.modelValue) ? props.modelValue : []
);

watch(
  () => props.modelValue,
  (newVal) => {
    if (Array.isArray(newVal)) {
      localRange.value = newVal;
    }
  }
);

const updateModel = (event: Event) => {
  const name = (event.target as HTMLInputElement).name;
  const value = (event.target as HTMLInputElement).value;
  emit("updateModel", name, value);
};

function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function onRangeChange(value: string[] | string) {
  if (Array.isArray(value) && value.length >= 2) {
    const startDate = formatDate(new Date(value[0]));
    const endDate = formatDate(new Date(value[value.length - 1]));
    emit("update", props.inputData.name, `${startDate} - ${endDate}`);
  } else {
    const singleDate = formatDate(new Date(value[0]));
    emit("update", props.inputData.name, `${singleDate} - ${singleDate}`);
  }
}

const handleInput = (event: Event) => {
  const name = (event.target as HTMLInputElement).name;
  const value = (event.target as HTMLInputElement).value;
  emit("update", name, value);
};
</script>

<style scoped lang="scss">
@use "@/assets/styles/style" as *;
@use "@/assets/styles/input.scss";

.input-wrapper > input[type="checkbox"] {
  flex-direction: row-reverse;
}

input[type="checkbox"] {
  margin: 1rem;
}

.error {
  border: 1px solid red;
}

.required::after {
  content: " *";
  color: red;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  margin: 1.5rem;
}

.input-label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.input {
  padding: 0.5rem;
  border-radius: 10px;
  font-size: 1rem;
  border: 1px solid rgba(0, 0, 0, 0.5);
}

input {
  padding: 1rem 0.75rem;
  border-radius: 0.5rem;
  width: 100%;
}

span {
  position: relative;
}

.showError {
  font-size: 0.7rem;
  display: block;
}

</style>
