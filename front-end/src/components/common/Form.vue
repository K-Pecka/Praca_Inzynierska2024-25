<script lang="ts" setup>
import FormInput from "@/components/common/FormInput.vue";
import {Input} from "@/types/interface";


const props = defineProps<{
  inputs: Input[];
  formValues: Record<string, string>;
  submitButtonLabel: string | undefined;
  disabled?: boolean;
}>();
const emit = defineEmits(["submitForm"]);
const updateState = (name: string, value: string) => props.formValues[name] = value;
const handleFieldUpdate = (name: string, value: string) => {
  props.formValues[name] = value;

  const input = props.inputs.find((input) => input.name === name);
  if (input) {
    input.error = [...input.validation.validate(value)];
    input.related?.forEach((el) => {
      let related = props.inputs.find((input) => input.name === el);
      if (related) {
        related.error = [...related.validation
            .isEqual(value)
            .validate(props.formValues[el])];
      }
    });
  }
  emit("submitForm", props.formValues);
};

const handleSubmit = () => {
  props.inputs.forEach(el => el.error = [...el.validation.validate(props.formValues[el.name])])
  emit("submitForm", props.formValues, {send: true});
};
</script>

<template>
  <v-col cols="12" md="6" lg="8" offset-md="3" offset-lg="2">
    <v-form validate-on="submit lazy" @submit.prevent="handleSubmit" class="form-container">
      <div v-for="(inputData, index) in inputs" :key="index">
        <FormInput
            :inputData="inputData"
            v-model="formValues[inputData.name]"
            @update="handleFieldUpdate"
            @update-model="updateState"
        />
      </div>
      <v-col>
        <v-row no-gutters>
          <v-btn type="submit" class="accept-form-button w-100" :disabled="props.disabled">{{ submitButtonLabel }}</v-btn>
        </v-row>
      </v-col>
      <div class="moreOption">
        <slot name="moreOption"></slot>
      </div>
    </v-form>
  </v-col>
</template>

<style scoped lang="scss">
@use "@/assets/styles/variables.scss" as *;

.accept-form-button {
  color: white !important;
  background-color: $background-primary !important;
}

.v-btn {
  color: rgba(var(--v-theme-text));
}

.form-container {
  background-color: rgba(var(--v-theme-secondary), 50%);
  padding: 0.25rem;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 15px;
}

.v-btn {
  margin-top: 0;
}

.moreOption {
  margin: 0 1.5rem 1.5rem 1.5rem;
}
</style>
