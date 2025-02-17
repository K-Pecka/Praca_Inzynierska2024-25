<script lang="ts" setup>
import { useUserStore } from "@/stores/userStore";
import {useMessageStore} from "@/stores/messageStore"
import { useRouter } from 'vue-router';
const router = useRouter();
const { logout } = useUserStore();
const {setSuccessCurrentMessage,logOutSuccess} = useMessageStore();
logout();
setSuccessCurrentMessage(logOutSuccess())
router.push('/');
</script>
<template></template>