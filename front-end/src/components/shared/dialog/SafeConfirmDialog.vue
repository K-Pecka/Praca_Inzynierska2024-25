<template>
  <v-dialog v-model="dialog" max-width="480" persistent>
    <v-card rounded="lg" elevation="2">
      <v-card-title class="text-h6 py-4 px-6">{{ title }}</v-card-title>

      <v-card-text class="px-6 py-4 text-body-1 text-medium-emphasis">
        <div>{{ message }}</div>

        <v-text-field
          v-if="wordToConfirm"
          v-model="input"
          variant="outlined"
          density="comfortable"
          class="mt-4"
          color="primary"
          :label="`Wpisz: ${wordToConfirm}`"
          :rules="[(v) => v === wordToConfirm || 'Niepoprawne słowo']"
          required
          clearable
        />
      </v-card-text>

      <v-card-actions class="px-4 pb-4">
        <v-spacer />
        <v-btn variant="text" color="gray" @click="cancel">Anuluj</v-btn>
        <v-btn
          variant="flat"
          color="delete"
          @click="confirm"
          :disabled="!!wordToConfirm && input !== wordToConfirm"
        >
          Potwierdź
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";

const dialog = ref(false);
const resolveFn = ref<((confirmed: boolean) => void) | null>(null);
const input = ref("");

const title = ref("Potwierdź usunięcie");
const message = ref("Czy na pewno chcesz kontynuować?");
const wordToConfirm = ref<string | undefined>(undefined);

function open(options?: { title?: string; message?: string; wordToConfirm?: string }) {
  title.value = options?.title || "Potwierdź usunięcie";
  message.value = options?.message || "Czy na pewno chcesz kontynuować?";
  wordToConfirm.value = options?.wordToConfirm;
  input.value = "";
  dialog.value = true;
  return new Promise<boolean>((resolve) => {
    resolveFn.value = resolve;
  });
}

function confirm() {
  dialog.value = false;
  resolveFn.value?.(true);
  resolveFn.value = null;
}

function cancel() {
  dialog.value = false;
  resolveFn.value?.(false);
  resolveFn.value = null;
}

defineExpose({ open });
</script>
