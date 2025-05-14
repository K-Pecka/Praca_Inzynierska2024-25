<template>
  <v-app class="bg-app">
    <SafeConfirmDialog ref="dialogRef" />
      <router-view />
  </v-app>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification';
import { watch } from 'vue';
import { useNotificationStore} from "@/stores";
import { toastConfig } from '@/lib';

import SafeConfirmDialog from "@/components/SafeConfirmDialog.vue";
import { useSafeDelete } from "@/composables/useSafeDelete";

import 'vue-toastification/dist/index.css';

const toast = useToast();
const messageStore = useNotificationStore();

// Dialog logic
const { dialogRef } = useSafeDelete();

watch(
  () => messageStore.errorCurrentMessage,
  (newMessage) => {
    if (newMessage) {
      toast.error(newMessage, toastConfig);
      messageStore.errorCurrentMessage = "";
    }
  }
);

watch(
  () => messageStore.successCurrentMessage,
  (newMessage) => {
    if (newMessage) {
      toast.success(newMessage, toastConfig);
      messageStore.successCurrentMessage = "";
    }
  }
);

</script>

<style lang="scss" scoped>
@use "@/assets/styles/variables" as *;

.text-primary {
 color: rgb($primary-color)
}
</style>