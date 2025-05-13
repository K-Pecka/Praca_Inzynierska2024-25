<script setup lang="ts">
import { ref, watch } from "vue";
import AppButton from "@/components/AppButton.vue";

const props = defineProps<{
  title?: string;
  dialog: boolean;
}>();

const emit = defineEmits(["submitForm", "update:dialog"]);

const emailInput = ref("");

// Resetuj pola po zamknięciu dialogu
watch(
  () => props.dialog,
  (val) => {
    if (!val) {
      emailInput.value = "";
    }
  }
);

function handleSubmit() {
  emit("submitForm", { email: emailInput.value });
}

function handleCancel() {
  emit("update:dialog", false);
}
</script>

<template>
  <v-dialog v-model="props.dialog" max-width="800">
    <v-card class="pa-2">
      <v-card-title class="text-h6">{{
        props.title ?? "Dodaj uczestnika"
      }}</v-card-title>
      <v-card-text>
        <v-container>
          <v-row dense no-gutters>
            <v-col cols="12">
              <v-text-field
                v-model="emailInput"
                variant="outlined"
                label="Adres email"
                placeholder="jan.kowalski@gmail.com"
                type="email"
                required
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="d-flex flex-column flex-sm-row">
        <AppButton color="accent" text="Anuluj" @click="handleCancel" />
        <AppButton color="primary" text="Dodaj" @click="handleSubmit" />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
