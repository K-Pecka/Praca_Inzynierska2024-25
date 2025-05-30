<template>
  <div class="input-wrapper">
  
    <template v-if="inputData.type === 'date_range'">
      <v-date-input
        v-model="localRange"
        :min="inputData.config?.min"
        :max="inputData.config?.max"
        :label="inputData.label"
        :placeholder = "!inputData.config?.min || !inputData.config?.maxDate ? inputData.placeholder : `${inputData.config?.min} - ${inputData.config?.maxDate}`"
        :multiple="inputData.config?.multiple ? 'range' : false"
        variant="outlined"
        prepend-icon=""
        prepend-inner-icon="mdi-calendar"
        bg-color="white"
        rounded="lg"
        @update:model-value="onRangeChange"
        color="primary"
        header-color="primary"
        :error="!!inputData.error?.length"
        :error-messages="inputData.error"
      />
    </template>

    <template v-else>
      <v-text-field
        v-model="inputValue"
        :type="inputData.type || 'text'"
        :name="inputData.name"
        :id="inputData.name"
        :label="inputData.label || inputData.config?.label"
        variant="outlined"
        :error="!!inputData.error?.length"
        :error-messages="inputData.error"
        @blur="handleInput"
        color="primary"
        bg-color="white"
        rounded="lg"
        :counter="inputData.config?.maxLength ?? undefined"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { VDateInput} from 'vuetify/labs/components'
import { Input } from '@/types/interface'

const {inputData,modelValue} = defineProps({
  inputData: {
    type: Object as () => Input,
    required: true,
  },
  modelValue: {
    type: [String, Array],
    default: '',
  },
})

const emit = defineEmits(['update', 'updateModel'])

const inputValue = ref(modelValue as string)
const localRange = ref<string[]>(Array.isArray(modelValue) 
  ? modelValue as string[] : []);
localRange.value = [
  inputData?.config?.min
    ? typeof inputData.config.min === 'string'
      ? inputData.config.min
      : formatDate(new Date(inputData.config.min))
    : '',
  inputData?.config?.maxDate
    ? typeof inputData.config.maxDate === 'string'
      ? inputData.config.maxDate
      : formatDate(new Date(inputData.config.maxDate))
    : ''
]
watch(() => modelValue, (newVal) => {
  if (typeof newVal === 'string') {
    inputValue.value = newVal
  } else if (Array.isArray(newVal)) {
    localRange.value = newVal as string[]
  }
})

watch(inputValue, (newVal) => {
  emit('updateModel', inputData.name, newVal)
})

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

function onRangeChange(value: string[] | string) {
  if (Array.isArray(value) && value.length >= 2) {
    const startDate = formatDate(new Date(value[0]))
    const endDate = formatDate(new Date(value[value.length - 1]))
    emit('update', inputData.name, `${startDate} - ${endDate}`)
  } else if (Array.isArray(value)) {
    const singleDate = formatDate(new Date(value[0]))
    emit('update', inputData.name, `${singleDate} - ${singleDate}`)
  }
}

function handleInput() {
  emit('update', inputData.name, inputValue.value)
}
if(localRange.value.length > 0 && inputData.type === 'date_range')
{
  console.log("tak",localRange.value)
  onRangeChange(localRange.value)
}
</script>

<style scoped lang="scss">
.required::after {
  content: " *";
  color: red;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  margin: 1.5rem;
}
</style>
