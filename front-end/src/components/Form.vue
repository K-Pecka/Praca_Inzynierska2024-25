<template>
  <v-container>
    <v-row class="wrapper">
      <v-col cols="12" md="6" lg="8" offset-md="3" offset-lg="2">
        <form @submit.prevent="handleSubmit" class="form-container">
          <div v-for="(inputData, index) in inputs" :key="index">
            <InputWithLabel
              :inputData="inputData"
              v-model="formValues[inputData.name]"
              @update="handleFieldUpdate"
            />
          </div>

          <button type="submit">{{ submitButtonLabel }}</button>
          <div class="moreOption">
            <slot name="moreOption"></slot>
          </div>
        </form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import InputWithLabel from "@/components/InputWithLabel.vue";

interface Config {
  required: Boolean;
}

export interface InputData {
  name: string;
  related?: string[];
  label: string;
  placeholder: string;
  validation: any;
  config?: Config;
  error: string[];
}

const props = defineProps<{
  inputs: InputData[];
  formValues: Record<string, string>;
  submitButtonLabel: string | undefined;
}>();

const emit = defineEmits(["submitForm"]);

const handleFieldUpdate = (name: string, value: string) => {
  props.formValues[name] = value;

  const input = props.inputs.find((input) => input.name === name);
  if (input) {
    console.log(">>========================");
    input.error = input.validation.validate(value);
    input.related?.forEach((el) => {
      let related = props.inputs.find((input) => input.name === el);
      console.log(related);
      if (related) {
        related.error = related.validation
          .isEqual(value)
          .validate(props.formValues[el]);
      }
    });

    console.log("========================<<");
  }
  emit("submitForm", props.formValues);
};

const handleSubmit = () => {
  emit("submitForm", props.formValues, { send: true });
};
</script>

<style scoped lang="scss">
.form-container {
  background-color: rgba(var(--rgb-secondary-color), 0.9);
  padding: 0.25rem;
  border-radius: 0.5rem;
}

button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  width: calc(100% - 3rem);
  padding: 0.75rem;
  margin: 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
}
button{
  margin-top: 0;
}
.moreOption {
  margin: 0 1.5rem 1.5rem 1.5rem;
}
</style>
