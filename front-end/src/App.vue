<template>
  <v-app class="bg-app application--wrap">
      <router-view />
  </v-app>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification';
import { watch } from 'vue';
import { useNotificationStore} from "@/stores";
import { toastConfig } from '@/lib';
import 'vue-toastification/dist/index.css';

const toast = useToast();
const messageStore = useNotificationStore();

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

.bg-app {
  background-color: rgb(var(--v-theme-background));
}
.application--wrap{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.text-primary {
 color: $primary-color
}
</style>