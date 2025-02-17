<template>
  <router-view />
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification';
import { watch } from 'vue';
import { useMessageStore } from "@/stores";
import {toastConfig} from '@/lib/toast.ts';
import 'vue-toastification/dist/index.css';

const toast = useToast();
const messageStore = useMessageStore();
const configToast = toastConfig;
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
      messageStore.successCurrentMessage = "";
    }
  }
);
</script>
