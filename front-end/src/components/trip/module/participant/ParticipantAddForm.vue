<script setup lang="ts">
import {ref} from "vue";
import AppButton from "@/components/AppButton.vue";

const props = defineProps<{ title?: string }>();

const emit = defineEmits(["submitForm", "cancel"]);

const nameInput = ref("");
const emailInput = ref("");

function handleSubmit() {
  emit("submitForm", {name:nameInput.value, email:emailInput.value});
  nameInput.value = "";
  emailInput.value = "";
  emit("cancel");
}

function handleCancel() {
  emit("cancel");
}
</script>

<template>
  <div class="add-participant-card">
    <div class="wrapper">
    <h3 class="card-title">{{ props.title }}</h3>

    <div class="form-fields">
      <div class="field">
        <label>Imię i nazwisko</label>
        <input v-model="nameInput" placeholder="Jan Kowalski" type="text"/>
      </div>
      <div class="field">
        <label>Adres email</label>
        <input v-model="emailInput" placeholder="jan.kowalski@gmail.com" type="email"/>
      </div>
    </div>

    <div class="form-buttons pt-3">
      <AppButton
          color="secondary"
          text="Anuluj"
          @click="handleCancel"
      />
      <AppButton
          color="primary"
          text="Dodaj"
          @click="handleSubmit"
      />
    </div>
  </div>
  </div>
  
</template>

<style scoped lang="scss">
.wrapper{
  min-width: 75%;
  max-width: 80%;
}
@media (min-width: 1200px){
  .wrapper{
    min-width: 35%;
    max-width: 40%;
  }
  
}
.add-participant-card {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(var(--v-theme-secondary), 0.5);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.card-title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.form-fields {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  flex: 1;
}

label {
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
@media (max-width: 600px) {
  .form-fields{
    flex-direction: column;
  }
  .form-buttons {
    justify-content:center;
    align-items: stretch;
  }
  
  .field {
    flex: 1;
  }
}
</style>
