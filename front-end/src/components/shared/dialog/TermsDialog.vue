<template>
  <v-dialog v-model="modelValue" :max-width="maxWidth ?? '500px'">
    <v-card>
      <v-card-title class="text-h6 d-flex justify-space-between align-center">
        {{ title }}
        <v-btn size="24" @click="cancelDialog" v-if="showCloseButton" variant="flat" icon>
          <v-icon size="24">mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-divider />

      <v-card-text style="max-height: 300px; overflow-y: auto;">
        <slot name="content">
          <ol class="pl-4">
            <li
              v-for="(point, index) in defaultPoints"
              :key="index"
              class="mb-2"
            >
              {{ point }}
            </li>
          </ol>
        </slot>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-spacer />
        <v-btn color="accent" text @click="cancelDialog" v-if="showCancel">
          Anuluj
        </v-btn>
        <v-btn color="primary" @click="acceptTerms">
          {{ acceptButtonText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">

const emit = defineEmits(["accepted", "cancel"]);

const props = defineProps<{
  modelValue: boolean;
  title?: string;
  acceptButtonText?: string;
  showCancel?: boolean;
  showCloseButton?: boolean;
  maxWidth?: string;
  points?: string[];
}>();

const modelValue = defineModel<boolean>();

const cancelDialog = () => {
  emit("cancel");
  modelValue.value = false;
};

const acceptTerms = () => {
  emit("accepted");
  modelValue.value = false;
};

const defaultPoints = props.points ?? [
  "Dane osobowe są przetwarzane zgodnie z obowiązującymi przepisami RODO.",
  "Niedozwolone jest tworzenie kont w celu ich późniejszego usunięcia bez powodu.",
  "Administrator ma prawo do usunięcia konta bez podania przyczyny w przypadku naruszenia regulaminu.",
  "Korzystanie z systemu oznacza akceptację warunków."
];
</script>
