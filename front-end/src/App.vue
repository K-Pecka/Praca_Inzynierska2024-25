<template>
  <router-view />
</template>

<script setup lang="ts">
import { useToast, POSITION } from 'vue-toastification';
import { watch } from 'vue';
import { useMessageStore } from './stores/messageStore';
import 'vue-toastification/dist/index.css';

const toast = useToast();
const messageStore = useMessageStore();
const configToast = {
        position: POSITION.BOTTOM_RIGHT,
        timeout: 5048,
        closeOnClick: true,
        pauseOnFocusLoss: false,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 2,
        showCloseButtonOnHover: false,
        hideProgressBar: false,
        closeButton: "button" as keyof HTMLElementTagNameMap,
        icon: true,
        rtl: false
      };
watch(
  () => messageStore.errorCurrentMessage,
  (newMessage) => {
    if (newMessage) {
      toast.error(newMessage, configToast);
      messageStore.errorCurrentMessage = "";
    }
  }
);
watch(
  () => messageStore.successCurrentMessage,
  (newMessage) => {
    if (newMessage) {
      toast.success(newMessage, configToast);
      messageStore.errorCurrentMessage = "";
    }
  }
);
</script>

<style scoped>
</style>
