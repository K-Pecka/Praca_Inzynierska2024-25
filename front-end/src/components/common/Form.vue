<template>
  <v-container>
    <v-row class="wrapper">
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
          <v-btn type="submit" color="white">{{ submitButtonLabel }}</v-btn>
          <div class="moreOption">
            <slot name="moreOption"></slot>
          </div>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import FormInput from "@/components/common/FormInput.vue";
import { Input } from "@/types/interface";


const props = defineProps<{
  inputs: Input[];
  formValues: Record<string, string>;
  submitButtonLabel: string | undefined;
}>();
const emit = defineEmits(["submitForm"]);
const updateState = (name: string, value: string) =>props.formValues[name] = value;
const handleFieldUpdate = (name: string, value: string) => {
  props.formValues[name] = value;
  
  const input = props.inputs.find((input) => input.name === name);
  //console.log(props.formValues)
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
  props.inputs.forEach(el => el.error=[...el.validation.validate(props.formValues[el.name])])
  emit("submitForm", props.formValues, { send: true });
};
</script>

<style scoped lang="scss">
.v-btn{
  color:rgba(var(--v-theme-text));
}
.form-container {
  background-color: rgba(var(--v-theme-secondary),50%);
  padding: 0.25rem;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 15px;
}

.v-btn {
  background-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-text));
  width: calc(100% - 3rem);
  height: 3rem;
  margin: 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 17px;
  cursor: pointer;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  text-transform: none;
  font-weight: bold;
}
.v-btn{
  margin-top: 0;
}
.moreOption {
  margin: 0 1.5rem 1.5rem 1.5rem;
}
</style>
